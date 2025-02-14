from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    website_slides_create_user = fields.Boolean(
        string="Create user",
        config_parameter="channel.create_user",
    )

    module_website_slides_edu = fields.Boolean(string="Edu")
