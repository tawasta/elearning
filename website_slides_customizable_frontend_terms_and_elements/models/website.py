from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    slide_channel_search_field_placeholder_term = fields.Char(
        string="eLearning Search Field Placeholder Term",
        translate=True,
        default="Search courses...",
        help="Override the default 'Search courses...'",
    )

    slide_channel_all_slides_link_term = fields.Char(
        string="eLearning Home All Slides Term",
        translate=True,
        default="All Courses",
        help="Override the default link text 'All courses' in eLearning home view",
    )

    slide_channel_breadcrumb_term = fields.Char(
        string="eLearning Breadcrumb Term",
        translate=True,
        default="Courses",
        help="Override the default breadcrumb item 'Courses'",
    )

    slide_channel_hide_tag_groups = fields.Boolean(
        string="Hide Tag Group Drowdown",
        help="Hide the dropdown that contains by default 'Your Level' related tags",
    )

    slide_channel_hide_aside_content = fields.Boolean(
        string="Hide Sidebar with Profile, Badges etc.",
        help="Hide the right sidebar contents from courses homepage",
    )
