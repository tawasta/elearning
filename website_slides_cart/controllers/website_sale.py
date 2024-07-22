# 1. Standard library imports:
from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale

# 2. Known third party imports:
# 3. Odoo imports (openerp):
# 4. Imports from Odoo modules:


class WebsiteSale(WebsiteSale):
    @http.route()
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        res = super(WebsiteSale, self).cart_update(product_id, add_qty, set_qty)
        if kw.get("return_course_url"):
            return request.redirect(kw.get("return_course_url"))
        else:
            return res
