##############################################################################
#
#    Author: Tawasta
#    Copyright 2020 Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################
{
    "name": "Website Slides Core",
    "summary": "Website Slides Core",
    "version": "17.0.1.0.0",
    "category": "Website",
    "website": "https://gitlab.com/tawasta/odoo/elearning",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["website_slides"],
    "data": [
        "data/mail_data.xml",
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/slide_channel_partner_views.xml",
        "views/slide_channel_views.xml",
        "views/website_slides_templates_lesson.xml",
        "wizard/slide_channel_feedback_views.xml",
    ],
    "demo": [],
}
