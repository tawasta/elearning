from odoo import models, fields
from datetime import timedelta
import logging
import pytz

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

        fin_tz = pytz.timezone('Europe/Helsinki')

        for rec in new_failures:
            retry_delay = rec.slide_partner_id.channel_id.retry_delay_hours or 0

            now_utc = fields.Datetime.now()
            now_local = now_utc.replace(tzinfo=pytz.UTC).astimezone(fin_tz).replace(tzinfo=None)
            retry_after_local = now_local + timedelta(hours=retry_delay)

            rec.slide_partner_id.write({
                "last_failed_attempt": now_local,
                "next_retry_possible_at": retry_after_local,
            })

        return res
