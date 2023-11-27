from odoo import models
from werkzeug import urls


class Slide(models.Model):
    _inherit = "slide.slide"

    def _find_document_data_from_url(self, url):
        res = super()._find_document_data_from_url(url)
        url_obj = urls.url_parse(url)
        if url_obj.ascii_host == 'vimeo.com':
            res = ('vimeo', url_obj.path[1:] if url_obj.path else False)

        return res

    def _parse_vimeo_document(self, document_id, only_preview_fields):
        # Method 1: fetching direct video link (response is difficult to parse)
        # fetch_res = self._fetch_data("https://player.vimeo.com/video/734265139", {})

        # Method 2: fetching video XML
        url = f"https://vimeo.com/api/v2/video/{document_id}.xml"
        fetch_res = self._fetch_data(url, {})

        # Method 3: using vimeo API (this would allow us to use private videos)

