# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import re

from odoo import _
from odoo import api
from odoo import fields
from odoo import models
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
        "res.partner", string="Recipients", compute="_get_attendees",
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
    def _get_attendees(self):
        for feedback in self:
            if feedback.template_id:
                feedback.partner_ids = feedback.channel_id.partner_ids.ids
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
            channel_partner = (
                self.env["slide.channel.partner"]
                .sudo()
                .search(
                    [
                        ("channel_id", "=", self.channel_id.id),
                        ("partner_id", "=", partner.id),
                    ]
                )
            )
            message_template = self.template_id
            mail_values = {
                "email_from": self.env.user.email_formatted,
                "subject": self.subject,
                "body_html": self.body,
                "email_to": partner.email,
                "attachment_ids": self.attachment_ids.ids,
            }

            subject = self.subject
            body = self.body
            message_template.sudo().write(mail_values)
            message_template.sudo().send_mail(channel_partner.id, force_send=True)
            print(message_template)
            message = channel_partner.message_ids
            print(message)

            # channel_partner.message_post(body=self.body, subject=self.subject, subtype_xmlid='mail.mt_comment', partner_ids=[partner.id], attachment_ids=self.attachment_ids.ids)

            channel_partner.with_context(mail_create_nosubscribe=True).message_post(
                subject=subject,
                body=body,
                attachment_ids=self.attachment_ids.ids,
                subtype_xmlid="website_slides.mail_template_slide_channel_feedback",
                # email_layout_xmlid='mail.mail_notification_light',
                # **kwargs,
            )

        return {"type": "ir.actions.act_window_close"}
