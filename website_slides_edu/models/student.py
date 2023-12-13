from odoo import _, fields, models


class OpStudent(models.Model):
    _inherit = "op.student"

    slide_channel_ids = fields.Many2many(
        "slide.channel",
        "slide_channel_student",
        "partner_id",
        "channel_id",
        string="eLearning Courses",
    )
    slide_channel_count = fields.Integer(
        "Course Count", compute="_compute_slide_channel_count"
    )

    def _compute_slide_channel_count(self):
        student_courses = (
            self.env["slide.channel.partner"]
            .sudo()
            .search_count([("partner_id", "=", self.partner_id.id)])
        )

        for student in self:
            student.slide_channel_count = student_courses

    def action_view_courses(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "website_slides.slide_channel_action_overview"
        )
        action["name"] = _("Followed Courses")
        action["domain"] = [
            "|",
            ("partner_ids", "in", self.partner_id.ids),
            ("partner_ids", "in", self.partner_id.child_ids.ids),
        ]
        return action
