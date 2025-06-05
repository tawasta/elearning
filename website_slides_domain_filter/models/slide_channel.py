from odoo import models, fields, http, _
from odoo.http import request
from odoo.tools.safe_eval import safe_eval
import logging

_logger = logging.getLogger(__name__)


class Channel(models.Model):
    _inherit = "slide.channel"

    partner_domain_filter_ids = fields.Many2many(
        "partner.domain.filter",
        string="Partner filters",
    )

    user_in_partner_domain = fields.Boolean(
        string="User has access to this product",
        compute="_compute_user_in_partner_domain",
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
        # Haetaan kaikki channel-id:t tuloksista
        result_ids = [r["id"] for r in results_data]
        # Ladataan ne channel-recordit ORM:llä
        channels = self.browse(result_ids).filtered(lambda c: c.user_in_partner_domain)
        allowed_ids = set(channels.ids)
        # Suodatetaan pois ne dictit, joiden id ei ole allowed_ids-joukossa
        filtered_results = [r for r in results_data if r["id"] in allowed_ids]

        return filtered_results
