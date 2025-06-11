from odoo import models, fields, api
from odoo.exceptions import AccessError

class SlideSlide(models.Model):
    _inherit = 'slide.slide'

    required_previous_slide_ids = fields.Many2many(
        'slide.slide',
        'slide_slide_required_prev_rel',
        'slide_id',
        'required_slide_id',
        string="Required Previous Slides",
        domain="[('channel_id', '=', channel_id)]",
        help="These slides must be completed before this slide can be accessed."
    )

    def _check_slide_access(self, partner_id):
        """Raise AccessError if required slides have not been completed by partner"""
        SlidePartner = self.env['slide.slide.partner']
        for slide in self:
            required_slides = slide.required_previous_slide_ids
            if not required_slides:
                continue

            completed_slides = SlidePartner.search([
                ('partner_id', '=', partner_id.id),
                ('slide_id', 'in', required_slides.ids),
                ('completed', '=', True)
            ]).mapped('slide_id')

            missing_slides = set(required_slides.ids) - set(completed_slides.ids)
            if missing_slides:
                raise AccessError("You must complete required previous sections before accessing this one.")
