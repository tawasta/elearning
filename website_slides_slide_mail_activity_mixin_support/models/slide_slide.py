from odoo import models


class Slide(models.Model):

    _name = "slide.slide"
    _inherit = ["slide.slide", "mail.activity.mixin"]
