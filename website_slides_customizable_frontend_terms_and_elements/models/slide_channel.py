from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SlideChannel(models.Model):
    _inherit = "slide.channel"

    hide_course_sidebar = fields.Boolean(
        string="Hide Course's Sidebar Entirely",
        help="Hides the left sidebar with Last updated, Responsible person etc. info",
    )

    hide_course_sidebar_responsible = fields.Boolean(
        string="Hide 'Responsible' from Course's Sidebar",
        help="Keep sidebar but hide single field",
    )

    hide_course_sidebar_members = fields.Boolean(
        string="Hide 'Members' from Course's Sidebar",
        help="Keep sidebar but hide single field",
    )

    hide_section_lesson_count_and_completion_time = fields.Boolean(
        string="Hide Lesson Count and Completion Time from Course Sections",
        help="Hides the '1h 45min' and 'x Lessons' text from section headers",
    )

    fullscreen_menu_lessons_term = fields.Char(
        string="Lessons List Term in Fullscreen Viewer",
        translate=True,
        default="Lessons",
        help="Override the default term 'Lessons' at top left of fullscreen viewer",
    )

    fullscreen_menu_back_to_course_term = fields.Char(
        string="Back to Course Term in Fullscreen Viewer",
        translate=True,
        default="Back to Course",
        help="Override the default term 'Back to Course' at top right of fullscreen viewer",
    )

    @api.constrains(
        "hide_course_sidebar",
        "hide_course_sidebar_responsible",
        "hide_course_sidebar_members",
    )
    def _check_sidebar_hiding_settings(self):
        for record in self:
            if record.hide_course_sidebar and (
                record.hide_course_sidebar_responsible
                or record.hide_course_sidebar_members
            ):
                raise ValidationError(
                    _(
                        "Can't hide sidebar elements individually if entire sidebar "
                        "is hidden."
                    )
                )
