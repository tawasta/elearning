##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2023 Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
    "name": "Website Slides - Sort content by category",
    "summary": "Provides better categorizing/sorting functionalities for slides",
    "version": "14.0.1.1.0",
    "category": "Document Management",
    "website": "https://gitlab.com/tawasta/odoo/elearning",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_slides",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/slide_slide_views.xml",
        "wizard/slides_choose_category_wizard.xml",
        "wizard/channels_reorder_categories_wizard.xml",
    ],
}
