from odoo import models, fields, api


class SlideSlidePartner(models.Model):
    _inherit = "slide.slide.partner"

    last_failed_attempt = fields.Datetime("Last Failed Attempt", readonly=True)
    next_retry_possible_at = fields.Datetime("Next Retry Allowed At")

    next_retry_local = fields.Datetime(
        string='Next Retry (Local Time)',
        compute='_compute_next_retry_local',
        store=False,
    )

    @api.depends('next_retry_possible_at')
    def _compute_next_retry_local(self):
        for rec in self:
            if rec.next_retry_possible_at:
                dt_aware = fields.Datetime.context_timestamp(self.env.user, rec.next_retry_possible_at)
                rec.next_retry_local = dt_aware.replace(tzinfo=None) if dt_aware else False
            else:
                rec.next_retry_local = False