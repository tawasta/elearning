from odoo import models, fields

class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    retry_delay_hours = fields.Integer(
        string="Retry Delay (hours)",
        default=24,
        help="How many hours the user must wait after a failed certification before retrying."
    )
