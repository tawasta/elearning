from odoo import fields, models


class ChannelsReorderCategoriesWizardCategory(models.TransientModel):

    _name = "channels.reorder.categories.wizard.category"
    _rec_name = "original_name"
    _order = "sequence asc"

    sequence = fields.Integer("Sequence")

    reorder_wizard_id = fields.Many2one(
        comodel_name="channels.reorder.categories.wizard",
        string="Category Reordering Wizard",
    )

    original_id = fields.Integer(string="Original ID")

    original_name = fields.Char(string="Original Name")

    original_sequence = fields.Integer(string="Original Sequence")
