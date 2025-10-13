from odoo import models, fields, http, _
from odoo.http import request
from odoo.tools.safe_eval import safe_eval
import logging

_logger = logging.getLogger(__name__)


class Channel(models.Model):
    _inherit = "slide.channel"

    partner_domain_mode = fields.Selection(
        [
            ("hide_channel", "Hide course from non-matching users"),
            ("hide_cta", "Show course, hide Join/Buy for non-matching users"),
        ],
        string="Partner filter behavior",
        default="hide_channel",
        help=(
            "Controls what partner domain filters do:\n"
            "- Hide course: non-matching users cannot see or open the course.\n"
            "- Hide Join/Buy: course page is visible, but Join/Buy is hidden and server-side enrollment/purchase is blocked."
        ),
    )

    user_can_see_channel = fields.Boolean(
        compute="_compute_partner_visibility_bits",
        string="User can see course",
    )

    hide_partner_cta = fields.Boolean(
        compute="_compute_partner_visibility_bits",
        string="Hide Join/Buy buttons for user",
    )

    partner_domain_filter_ids = fields.Many2many(
        "partner.domain.filter",
        string="Partner filters",
    )

    user_in_partner_domain = fields.Boolean(
        string="User has access to this product",
        compute="_compute_user_in_partner_domain",
    )

    def _compute_partner_visibility_bits(self):
        for rec in self:
            has_filters = bool(rec.partner_domain_filter_ids)
            in_domain = bool(rec.user_in_partner_domain)

            if not has_filters:
                rec.user_can_see_channel = True
            elif rec.partner_domain_mode == "hide_channel":
                rec.user_can_see_channel = in_domain
            else:
                rec.user_can_see_channel = True

            rec.hide_partner_cta = (
                has_filters and not in_domain and rec.partner_domain_mode == "hide_cta"
            )

    def _compute_user_in_partner_domain(self):
        partner = self.env["res.partner"].sudo()
        user_partner_id = self.env.user.partner_id.id
        for record in self:
            user_in_partner_domain = False
            for partner_domain in record.partner_domain_filter_ids:
                domain = [("id", "=", user_partner_id)] + safe_eval(
                    partner_domain.filter_domain
                )
                if partner.search(domain):
                    user_in_partner_domain = True

            record.user_in_partner_domain = (
                user_in_partner_domain or not record.partner_domain_filter_ids
            )

    def _search_render_results(self, fetch_fields, mapping, icon, limit):
        results_data = super()._search_render_results(
            fetch_fields, mapping, icon, limit
        )
        result_ids = [r["id"] for r in results_data]
        channels = self.browse(result_ids)

        allowed_ids = set(channels.filtered(lambda c: c.user_can_see_channel).ids)
        filtered_results = [r for r in results_data if r["id"] in allowed_ids]

        return filtered_results
