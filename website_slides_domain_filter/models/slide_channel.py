from odoo import models, fields, http, _
from odoo.http import request
from odoo.tools.safe_eval import safe_eval
import logging

_logger = logging.getLogger(__name__)

class Channel(models.Model):
    _inherit = 'slide.channel'

    paywall_domain = fields.Char(
        string="Paywall Domain",
        help="Comma-separated domains for which this ticket is visible."
    )

    user_in_paywall_domain = fields.Boolean(
        string="User has access to paywall content",
        compute="_compute_user_in_paywall_domain",
    )

    def _compute_user_in_paywall_domain(self):
        partner = self.env["res.partner"].sudo()
        partner_id = self.env.user.partner_id.id

        for record in self:
            paywall_domain = False
            if record.paywall_domain:
                paywall_domain = [("id", "=", partner_id)] + safe_eval(
                    record.paywall_domain
                )

            if paywall_domain and partner.search(paywall_domain):
                record.user_in_paywall_domain = True
            else:
                record.user_in_paywall_domain = False

    def _search_render_results(self, fetch_fields, mapping, icon, limit):
        results_data = super()._search_render_results(fetch_fields, mapping, icon, limit)
        # Haetaan kaikki channel-id:t tuloksista
        result_ids = [r['id'] for r in results_data]
        # Ladataan ne channel-recordit ORM:llä
        channels = self.browse(result_ids).filtered(
            lambda c: not c.paywall_domain or c.user_in_paywall_domain
        )
        allowed_ids = set(channels.ids)
        # Suodatetaan pois ne dictit, joiden id ei ole allowed_ids-joukossa
        filtered_results = [r for r in results_data if r['id'] in allowed_ids]

        return filtered_results

