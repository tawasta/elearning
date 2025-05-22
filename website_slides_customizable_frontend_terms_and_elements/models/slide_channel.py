from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SlideChannel(models.Model):
    _inherit = "slide.channel"

    hide_course_sidebar = fields.Boolean(
        string="Hide Course's Sidebar",
        help="Hides the left sidebar with Last updated, Responsible person etc. info",
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
