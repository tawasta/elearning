from odoo import fields, models


class SlidesChooseCategoryWizard(models.TransientModel):

    _name = "slides.choose.category.wizard"
    _description = "Slides Choose Category Wizard"

    slide_ids = fields.Many2many('slide.slide', string="Contents", default=lambda self: self.default_slides())
    channel_ids = fields.Many2many('slide.channel', default=lambda self: self.default_channels())
    category_sort_id = fields.Many2one('slide.slide', string="Choose a section",
            domain=lambda self: self.category_sort_id_domain())

    def default_slides(self):
        return self.env["slide.slide"].browse(self._context.get("active_ids"))

    def default_channels(self):
        """Use only channels related to the chosen documents"""
        channels = self.env["slide.channel"]

        for slide in self.slide_ids:
            channels += slide.channel_id
        return channels

    def category_sort_id_domain(self):
        return "[('is_category', '=', True), ('channel_id', 'in', {})]".format(self.new().channel_ids.ids)

    def confirm(self):
        """Mass operation done to documents (slides)"""
        slides = self.slide_ids

        slides.write({'category_sort_id': self.category_sort_id.id})

        # Recompute category_id of all slides
        all_slides = self.env['slide.slide'].search([])
        all_slides._compute_category_id()
