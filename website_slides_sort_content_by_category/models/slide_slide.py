from odoo import api, fields, models


class SlideSlide(models.Model):

    _inherit = "slide.slide"

    category_sort_id = fields.Many2one(
        "slide.slide", string="Choose a section", store=True
    )

    @api.depends(
        "channel_id.slide_ids.is_category",
        "channel_id.slide_ids.sequence",
        "category_sort_id",
    )
    def _compute_category_id(self):
        res = super()._compute_category_id()
        # Force a chosen category
        for slide in self:
            if slide.category_sort_id:
                slide.category_id = slide.category_sort_id
        return res

    @api.model
    def create(self, vals):
        category_sort_id = vals.get("category_sort_id")
        if category_sort_id:
            category_sort_id = self.env["slide.slide"].browse(category_sort_id)
            vals["sequence"] = category_sort_id.sequence + 1

        is_category = vals.get("is_category")
        if is_category:
            channel_id = vals.get("channel_id")
            slides = self.env["slide.slide"].search(
                [("channel_id", "=", channel_id)], order="sequence"
            )
            if slides:
                # Negative values are possible
                vals["sequence"] = slides[0].sequence - 1

        return super().create(vals)

    def write(self, vals):
        res = super().write(vals)
        category_sort_id = vals.get("category_sort_id")
        if category_sort_id:
            category_sort_id = self.env["slide.slide"].browse(category_sort_id)
            vals["sequence"] = category_sort_id.sequence + 1
        return res

    @api.onchange("category_sort_id")
    def onchange_category_sort_id(self):
        self.sequence = self.category_sort_id.sequence + 1
