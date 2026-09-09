from odoo import models


class SlideChannelInvite(models.TransientModel):
    _inherit = "slide.channel.invite"

    def _prepare_mail_values(self, slide_channel_partner):
        """Use the mail template's From address instead of the acting user's.

        Core hardcodes the sender as env.user.email_formatted and never reads
        the template's email_from, because slide.channel.invite wizard inherits
        the mail.composer.mixin which carries no sender field."""
        values = super()._prepare_mail_values(slide_channel_partner)

        if not self.template_id.email_from:
            return values

        # The field holds placeholders, so it has to be rendered, not copied
        email_from = self.template_id._render_field(
            "email_from", slide_channel_partner.ids
        )[slide_channel_partner.id]

        # An expression could render empty, in which case don't override
        if email_from.strip():
            values["email_from"] = email_from

        return values
