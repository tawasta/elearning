from odoo import fields
from odoo import models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    website_slides_create_user = fields.Boolean(
        string="Create user", config_parameter="channel.create_user",
    )

    module_website_slides_edu = fields.Boolean(string="Edu")

    lms_sender_address = fields.Char(string="LMS sender address", config_parameter='lms_sender_address')
