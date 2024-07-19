from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SlideChannel(models.Model):
    _inherit = "slide.channel"

    feedback_survey_id = fields.Many2one(
        string="Feedback survey", comodel_name="survey.survey"
    )

    def _action_add_members(self, target_partners, **member_values):
        response = super(SlideChannel, self)._action_add_members(
            target_partners, **member_values
        )
        for r in response:
            values = {
                "name": r.partner_id.name,
                "partner_id": r.partner_id.id,
                "login": r.partner_id.email,
            }
            get_param = self.env["ir.config_parameter"].sudo().get_param
            channel_create_user_param = get_param("channel.create_user")
            if channel_create_user_param == "True":
                if r.partner_id:
                    values = {
                        "name": r.partner_id.name,
                        "partner_id": r.partner_id.id,
                        "login": r.partner_id.email,
                    }
                    partner_user = (
                        r.partner_id.user_ids and r.partner_id.user_ids[0] or False
                    )
                    if not partner_user:
                        new_user = self.env["res.users"]._signup_create_user(values)
                        if new_user:
                            new_user.with_context(
                                create_user=True
                            ).action_reset_password()
            else:
                return r

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            allready_selected = (
                self.env["slide.channel"]
                .sudo()
                .search([("product_id", "=", self.product_id.id)])
            )
            if allready_selected:
                raise ValidationError(
                    _(
                        "You cannot select that product because "
                        "the product is already in use in another course. "
                        "Choose another product or create a new one. "
                    )
                )

    def action_channel_feedback(self):
        self.ensure_one()
        template = self.env.ref(
            "website_slides_core.mail_template_slide_channel_feedback",
            raise_if_not_found=False,
        )

        local_context = dict(
            self.env.context,
            default_channel_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
        )
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "slide.channel.feedback",
            "target": "new",
            "context": local_context,
        }


class ChannelUsersRelation(models.Model):
    _name = "slide.channel.partner"
    _inherit = ["slide.channel.partner", "mail.thread"]
    _rec_name = "partner_email"
