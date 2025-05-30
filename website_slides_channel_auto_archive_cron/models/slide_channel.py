from odoo import _, api, fields, models

import logging

_logger = logging.getLogger(__name__)


class SlideChannel(models.Model):
    _inherit = "slide.channel"

    auto_archive_date = fields.Datetime(
        string="Automatically Archive the Course On",
        help="Scheduler will unpublish and archive the course on set date",
    )

    def action_archive_courses(self):
        now = fields.Datetime.now()

        channels_to_archive = self.search(
            [("auto_archive_date", "!=", False), ("auto_archive_date", "<", now)]
        )

        for channel in channels_to_archive:
            channel.write({"is_published": False, "active": False})

            channel.message_post(
                body=_("Course automatically unpublished and archived by scheduler.")
            )
