from dateutil.relativedelta import relativedelta
from markupsafe import Markup

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SlideChannel(models.Model):
    _inherit = "slide.channel"

    auto_remove_participant = fields.Boolean(
        string="Auto-remove Participant Access",
        default=False,
        help="If enabled, participants will be automatically removed from this "
        "course after the configured number of days have elapsed since "
        "they joined.",
    )
    auto_remove_participant_after_days = fields.Integer(
        string="Access Removed After (Days)",
        default=30,
        help="Number of days after which a participant is automatically "
        "removed from the course, counted from the day they joined.",
    )

    @api.constrains("auto_remove_participant", "auto_remove_participant_after_days")
    def _check_auto_remove_participant_after_days(self):
        for channel in self:
            if (
                channel.auto_remove_participant
                and channel.auto_remove_participant_after_days <= 0
            ):
                raise ValidationError(
                    _(
                        "When auto-removal of participants is enabled, the number "
                        "of days must be greater than zero (course: %(name)s).",
                        name=channel.name,
                    )
                )

    @api.model
    def _cron_auto_remove_participants(self):
        """Scheduled action: for every channel that has auto-removal enabled,
        find memberships older than the configured number of days, remove the
        participants from the course and post a chatter note linking to each
        removed partner.
        """
        channels = self.search(
            [
                ("auto_remove_participant", "=", True),
                ("auto_remove_participant_after_days", ">", 0),
            ]
        )
        if not channels:
            return

        SlideChannelPartner = self.env["slide.channel.partner"]
        now = fields.Datetime.now()

        for channel in channels:
            cutoff = now - relativedelta(
                days=channel.auto_remove_participant_after_days
            )
            expired_memberships = SlideChannelPartner.search(
                [
                    ("channel_id", "=", channel.id),
                    ("create_date", "<", cutoff),
                ]
            )
            for membership in expired_memberships:
                partner = membership.partner_id
                if not partner:
                    continue

                # Build an HTML link to the partner; using Markup with %-formatting
                # automatically escapes the display_name string.
                partner_link = Markup(
                    '<a href="#" data-oe-model="res.partner" data-oe-id="%d">%s</a>'
                ) % (partner.id, partner.display_name or "")
                body = Markup(
                    _(
                        "Participant %(partner)s has been automatically removed "
                        "from this course after %(days)s day(s)."
                    )
                ) % {
                    "partner": partner_link,
                    "days": channel.auto_remove_participant_after_days,
                }
                channel.message_post(body=body)
                channel._remove_membership(partner.ids)
