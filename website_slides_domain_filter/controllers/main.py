import logging

from odoo import http
from odoo.http import request
from odoo.addons.website_slides.controllers.main import WebsiteSlides
from werkzeug.exceptions import NotFound

_logger = logging.getLogger(__name__)


class WebsiteSlidesPaywall(WebsiteSlides):
    def slides_channel_all_values(
        self, slide_category=None, slug_tags=None, my=False, **post
    ):
        """
        Override default slide channel list logic to hide channels behind a paywall
        if user does not have access.
        """
        values = super().slides_channel_all_values(
            slide_category, slug_tags, my, **post
        )

        # Suodata pois kanavat, joihin käyttäjällä ei ole pääsyä
        channels = values.get("channels", request.env["slide.channel"])
        values["channels"] = channels.filtered(
            lambda c: not c.paywall_domain or c.user_in_paywall_domain
        )

        return values

    def slides_channel_home(self, **post):
        """
        Override slides home ("/slides") to hide paywall-protected channels.
        """
        response = super().slides_channel_home(**post)
        values = response.qcontext

        values["channels_my"] = values["channels_my"].filtered(
            lambda c: not c.paywall_domain or c.user_in_paywall_domain
        )

        values["channels_popular"] = values["channels_popular"].filtered(
            lambda c: not c.paywall_domain or c.user_in_paywall_domain
        )

        values["channels_newest"] = values["channels_newest"].filtered(
            lambda c: not c.paywall_domain or c.user_in_paywall_domain
        )

        return response

    @http.route()
    def channel(self, channel=False, channel_id=False, **kw):
        """
        Override channel route to block access to paywalled channels if user lacks access.
        """
        if channel_id and not channel:
            channel = request.env["slide.channel"].browse(channel_id).exists()

        if channel and channel.paywall_domain and not channel.user_in_paywall_domain:
            raise NotFound()

        return super().channel(channel=channel, channel_id=channel_id, **kw)
