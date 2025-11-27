from odoo import fields, models


class SlideChannel(models.Model):
    _inherit = "slide.channel"

    publish_template_id = fields.Many2one(default=False)
    share_channel_template_id = fields.Many2one(default=False)
    share_slide_template_id = fields.Many2one(default=False)
    completed_template_id = fields.Many2one(default=False)
