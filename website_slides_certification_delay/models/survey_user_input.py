from odoo import models, fields
from datetime import datetime, timedelta

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def write(self, vals):
        was_done_failures = self.filtered(lambda r: r.state == 'done' and not r.scoring_success and r.slide_partner_id)

        res = super().write(vals)

        now_failed = self.filtered(lambda r: r.state == 'done' and not r.scoring_success and r.slide_partner_id)
        new_failures = now_failed - was_done_failures

        for rec in new_failures:
            retry_delay = rec.slide_partner_id.channel_id.retry_delay_hours or 0
            retry_after = datetime.utcnow() + timedelta(hours=retry_delay)

            rec.slide_partner_id.write({
                'last_failed_attempt': fields.Datetime.now(),
                'next_retry_possible_at': retry_after,
            })

        return res
