from odoo import fields
from odoo import models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    website_slides_create_user = fields.Boolean(
        string="Create user", config_parameter="channel.create_user",
    )
