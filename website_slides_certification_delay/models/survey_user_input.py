import logging
from datetime import timedelta

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def write(self, vals):
        was_done_failures = self.filtered(
            lambda r: r.state == "done" and not r.scoring_success and r.slide_partner_id
        )

        res = super().write(vals)

        now_failed = self.filtered(
            lambda r: r.state == "done" and not r.scoring_success and r.slide_partner_id
        )
        new_failures = now_failed - was_done_failures

        for rec in new_failures:
            retry_delay = rec.slide_partner_id.channel_id.retry_delay_hours or 0

            now_utc = fields.Datetime.now()
            retry_after = now_utc + timedelta(hours=retry_delay)

            rec.slide_partner_id.write(
                {
                    "last_failed_attempt": now_utc,
                    "next_retry_possible_at": retry_after,
                }
            )

        return res
