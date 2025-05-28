.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
website slides domain filter
============================
This module adds paywall-style domain-based access control to *eLearning courses* (i.e. `slide.channel` records).

Users will only see courses (channels) if their partner record matches the defined `paywall_domain`.

Features
========

* Add a domain per course (channel)
* Users only see courses if their `res.partner` matches the domain
* Filters course visibility in:
  * Slide home page (`/slides`)
  * Search/autocomplete
  * Direct access to URL (blocks 404 if access denied)
* Backend field uses domain editor widget

Usage
=====

1. Go to **eLearning → Courses**
2. Open any course and add a `Partner filters`
3. Frontend visibility will automatically be filtered:
   * Courses are hidden from list pages, search results, and direct access

Technical details
=================

* `user_in_partner_domain`: computed Boolean based on the current user
* Slide controller (`/slides`) is overridden to filter `channel.home` and `channel`
* Autocomplete results are filtered at render time
* XML inherits the form view to include the `partner_domain_filter_ids` field with proper widget


Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>
* Jarmo Kortetjärvi <jarmo.kortetjarvi@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
