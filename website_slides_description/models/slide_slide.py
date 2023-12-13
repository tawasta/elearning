from odoo import fields, models
from odoo.tools.translate import html_translate


class SlideSlide(models.Model):
    _inherit = "slide.slide"

    website_description = fields.Html(
        "Website Description",
        sanitize_attributes=False,
        translate=html_translate,
        sanitize_form=False,
    )
