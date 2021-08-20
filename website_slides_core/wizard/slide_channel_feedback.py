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
        "slide.channel.partner", string="Recipients", compute="_get_attendees",
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
            message_template = self.template_id
            mail_values = {
                "email_from": self.env.user.email_formatted,
                "subject": self.subject,
                "body_html": self.body,
                "email_to": partner.partner_email,
                "attachment_ids": self.attachment_ids.ids,
            }

            message_template.sudo().send_mail(
                partner.id, email_values=mail_values, force_send=True
            )

        return {"type": "ir.actions.act_window_close"}
