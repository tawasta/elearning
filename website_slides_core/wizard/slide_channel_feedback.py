# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import re

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

emails_split = re.compile(r"[;,\n\r]+")


class SlideChannelFeedback(models.TransientModel):
    _name = "slide.channel.feedback"
    _description = "Channel Feedback Wizard"

    # composer content
    subject = fields.Char(
        "Subject", compute="_compute_subject", readonly=False, store=True
    )
    body = fields.Html(
        "Contents",
        sanitize_style=True,
        compute="_compute_body",
        readonly=False,
        store=True,
    )
    attachment_ids = fields.Many2many("ir.attachment", string="Attachments")
    template_id = fields.Many2one(
        "mail.template",
        "Use template",
        domain="[('model', '=', 'slide.channel.partner')]",
        readonly=True,
    )
    # recipients
    partner_ids = fields.Many2many(
        "slide.channel.partner",
        string="Recipients",
        compute="_compute_attendee_ids",
    )
    # slide channel
    channel_id = fields.Many2one("slide.channel", string="Slide channel", required=True)

    @api.depends("template_id")
    def _compute_subject(self):
        for feedback in self:
            if feedback.template_id:
                feedback.subject = feedback.template_id.subject
            elif not feedback.subject:
                feedback.subject = False

    @api.depends("template_id")
    def _compute_body(self):
        for feedback in self:
            if feedback.template_id:
                feedback.body = feedback.template_id.body_html
            elif not feedback.body:
                feedback.body = False

    @api.depends("template_id")
    def _compute_attendee_ids(self):
        for feedback in self:
            if feedback.template_id:
                feedback.partner_ids = feedback.channel_id.channel_partner_ids.ids
            elif not feedback.body:
                feedback.body = False

    def action_feedback(self):
        self.ensure_one()

        if not self.env.user.email:
            raise UserError(
                _(
                    "Unable to post message, please configure the sender's email address."
                )
            )

        mail_values = []
        for partner in self.partner_ids:
            mail_values.append(self._add_mail_values(partner))

        for mail_value in mail_values:
            new_mail = self.env["mail.mail"].sudo().create(mail_value)
            if new_mail:
                new_mail.send()

        return {"type": "ir.actions.act_window_close"}

    def _add_mail_values(self, partner):
        subject = self.env["mail.render.mixin"]._render_template(
            self.subject,
            "slide.channel.partner",
            partner.ids,
            options={"post_process": True},
        )[partner.id]
        body = self.env["mail.render.mixin"]._render_template(
            self.body,
            "slide.channel.partner",
            partner.ids,
            options={"post_process": True},
        )[partner.id]

        mail_values = {
            "email_from": self.env.user.email_formatted,
            "author_id": self.env.user.partner_id.id,
            "model": "slide.channel.partner",
            "res_id": partner.id,
            "subject": subject,
            "body_html": body,
            "attachment_ids": [(4, att.id) for att in self.attachment_ids],
            "auto_delete": True,
            "recipient_ids": [(4, partner.partner_id.id)],
        }
        mail_values["body_html"] = self.env["mail.render.mixin"]._replace_local_links(
            body
        )

        partner.sudo().message_post(
            message_type="comment",
            subtype_xmlid="mail.mt_note",
            subject=subject,
            body=body,
            attachment_ids=self.attachment_ids.ids,
        )

        return mail_values
