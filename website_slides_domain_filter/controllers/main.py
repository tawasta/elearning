from odoo import http, _
from odoo.http import request
from odoo.addons.website_slides.controllers.main import WebsiteSlides
from werkzeug.exceptions import NotFound


class WebsiteSlidesFilter(WebsiteSlides):
    def slides_channel_all_values(
        self, slide_category=None, slug_tags=None, my=False, **post
    ):
        """
        Extend slide channel value generation to respect partner-domain visibility.
        Only include channels that the current user is allowed to see.
        """
        values = super().slides_channel_all_values(
            slide_category, slug_tags, my, **post
        )

        channels = values.get("channels", request.env["slide.channel"])
        visible_channels = channels.filtered(lambda c: c.user_can_see_channel)
        values["channels"] = visible_channels
        return values

    def _filter_and_log(self, values, channel_list, label):
        """
        Helper to filter out channels the current user cannot see.
        """
        original = values.get(channel_list, request.env["slide.channel"])
        return original.filtered(lambda c: c.user_can_see_channel)

    @http.route()
    def slides_channel_home(self, **post):
        """
        Extend the slides home route ("/slides") to filter out channels
        that the current user should not see.
        """
        response = super().slides_channel_home(**post)
        values = response.qcontext

        values["channels_my"] = self._filter_and_log(
            values, "channels_my", "My channels"
        )
        values["channels_popular"] = self._filter_and_log(
            values, "channels_popular", "Popular channels"
        )
        values["channels_newest"] = self._filter_and_log(
            values, "channels_newest", "Newest channels"
        )

        return response

    @http.route()
    def channel(self, channel=False, channel_id=False, **kw):
        """
        Extend the channel route to apply partner-domain visibility logic:
        - hide_channel + no match → 404
        - hide_cta + no match → show page but hide CTA
        """
        if channel_id and not channel:
            channel = request.env["slide.channel"].browse(channel_id).exists()

        if (
            channel
            and (not channel.user_in_partner_domain)
            and channel.partner_domain_mode == "hide_channel"
        ):
            raise NotFound()

        response = super().channel(channel=channel, channel_id=channel_id, **kw)

        if channel:
            response.qcontext["hide_partner_cta"] = bool(channel.hide_partner_cta)

        return response
