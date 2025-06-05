import logging

from odoo import http
from odoo.http import request
from odoo.addons.website_slides.controllers.main import WebsiteSlides
from werkzeug.exceptions import NotFound

_logger = logging.getLogger(__name__)


class WebsiteSlidesFilter(WebsiteSlides):
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

        channels = values.get("channels", request.env["slide.channel"])
        accessible_channels = channels.filtered(lambda c: c.user_in_partner_domain)

        # Lokitus: kanavat joihin ei ole pääsyä
        for c in channels - accessible_channels:
            _logger.warning(
                "Käyttäjältä estetty pääsy kanavaan: %s (ID: %s), käyttäjä: %s (%s)",
                c.name, c.id, request.env.user.name, request.env.user.id,
            )

        # Lokitus: maksulliset kanavat joihin on pääsy
        for c in accessible_channels:
            if c.enroll == 'payment':
                try:
                    _logger.info(
                        "Näytetään maksullinen kanava: %s (ID: %s), tuote: %s, käyttäjä: %s (%s)",
                        c.name, c.id,
                        c.product_id.display_name if c.product_id else "Ei tuotetta",
                        request.env.user.name, request.env.user.id,
                    )
                except Exception as e:
                    _logger.error(
                        "Virhe tuotetiedon hakemisessa kanavalle %s (ID: %s): %s",
                        c.name, c.id, str(e),
                    )

        values["channels"] = accessible_channels
        return values

    def slides_channel_home(self, **post):
        """
        Override slides home ("/slides") to hide paywall-protected channels.
        """
        try:
            response = super().slides_channel_home(**post)
            values = response.qcontext

            def _filter_and_log(channel_list, label):
                original = values.get(channel_list, request.env["slide.channel"])
                filtered = original.filtered(lambda c: c.user_in_partner_domain)

                for c in original - filtered:
                    _logger.warning(
                        "Piilotetaan %s: %s (ID: %s), käyttäjältä ei ole pääsyä",
                        label, c.name, c.id
                    )

                return filtered

            values["channels_my"] = _filter_and_log("channels_my", "Omat kanavat")
            values["channels_popular"] = _filter_and_log("channels_popular", "Suositut kanavat")
            values["channels_newest"] = _filter_and_log("channels_newest", "Uusimmat kanavat")

            return response
        except Exception as e:
            _logger.exception("Virhe slides_channel_home käsittelyssä: %s", str(e))
            raise

    @http.route()
    def channel(self, channel=False, channel_id=False, **kw):
        """
        Override channel route to block access to filtered channels if user lacks access.
        """
        if channel_id and not channel:
            channel = request.env["slide.channel"].browse(channel_id).exists()

        if channel:
            if not channel.user_in_partner_domain:
                _logger.warning(
                    "Estetty pääsy kanavalle: %s (ID: %s), käyttäjä: %s (%s)",
                    channel.name, channel.id,
                    request.env.user.name, request.env.user.id,
                )
                raise NotFound()
            else:
                _logger.info(
                    "Käyttäjällä pääsy kanavalle: %s (ID: %s), enroll: %s",
                    channel.name, channel.id, channel.enroll
                )

                if channel.enroll == 'payment':
                    try:
                        _logger.info(
                            "Maksullinen kanava avattu: %s (ID: %s), tuote: %s",
                            channel.name, channel.id,
                            channel.product_id.display_name if channel.product_id else "Ei tuotetta",
                        )
                    except Exception as e:
                        _logger.error(
                            "Tuotetietojen luku epäonnistui kanavalle %s: %s", channel.name, str(e)
                        )

        return super().channel(channel=channel, channel_id=channel_id, **kw)
