from odoo import models, fields


class SlideSlidePartner(models.Model):
    _inherit = "slide.slide.partner"

    last_failed_attempt = fields.Datetime("Last Failed Attempt", readonly=True)
    next_retry_possible_at = fields.Datetime("Next Retry Allowed At")
