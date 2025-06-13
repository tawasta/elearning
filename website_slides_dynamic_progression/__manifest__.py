##############################################################################
#
#    Author: Futural Oy
#    Copyright 2023 Futural Oy (https://futural.fi)
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
    "name": "Website Slides Dynamic Progression",
    "summary": "Require completion of previous slides before accessing new ones",
    "version": "17.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/tawasta/elearning",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["website_slides"],
    "data": [
        "views/slide_form.xml",
        "views/website_slides_templates_course.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_slides_dynamic_progression/static/src/js/slides_course_page.esm.js",
            "website_slides_dynamic_progression/static/src/js/slides_course_quiz.esm.js",
        ],
    },
    "demo": [],
}
