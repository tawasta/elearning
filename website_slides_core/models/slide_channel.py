from odoo import _
from odoo import api
from odoo import models
from odoo.exceptions import Warning


class SlideChannel(models.Model):
    _inherit = "slide.channel"

    def _action_add_members(self, target_partners, **member_values):
        response = super(SlideChannel, self)._action_add_members(
            target_partners, **member_values
        )
        values = {
            "name": response.partner_id.name,
            "partner_id": response.partner_id.id,
            "login": response.partner_id.email,
        }
        get_param = self.env["ir.config_parameter"].sudo().get_param
        channel_create_user_param = get_param("channel.create_user")
        if channel_create_user_param == "True":
            if response.partner_id:
                values = {
                    "name": response.partner_id.name,
                    "partner_id": response.partner_id.id,
                    "login": response.partner_id.email,
                }
                partner_user = (
                    response.partner_id.user_ids
                    and response.partner_id.user_ids[0]
                    or False
                )
                if not partner_user:
                    new_user = self.env["res.users"]._signup_create_user(values)
                    if new_user:
                        new_user.with_context(create_user=True).action_reset_password()
        else:
            return response

    @api.onchange("product_id")
    def _onchange_product_id(self):
        allready_selected = (
            self.env["slide.channel"]
            .sudo()
            .search([("product_id", "=", self.product_id.id)])
        )
        if allready_selected:
            raise Warning(
                _(
                    "You cannot select that product because the product is already in use in another course. Choose another product or create a new one. "
                )
            )
