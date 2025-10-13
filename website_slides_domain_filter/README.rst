.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
website slides domain filter
============================
This module adds paywall-style domain-based access control to *eLearning courses* (i.e. `slide.channel` records).

Users will only see courses if their partner record matches the defined
**partner domain filter(s)**.

Features
========

* Add partner domain filters per course
* Choose filtering behavior:
  * **Hide course completely** (non-matching users cannot see or open it)
  * **Hide Join/Buy buttons only** (page visible, but enrollment disabled)
* Works seamlessly across:
  * Course listings (`/slides`)
  * Search and autocomplete results
  * Direct URL access to a course page
* Form view inherited to include the new partner-domain fields

Usage
=====

1. Go to **eLearning → Courses**
2. Open a course record
3. Set the **Partner filter behavior**:
   * *Hide course from non-matching users*
   * *Show course, hide Join/Buy for non-matching users*
4. Add one or more **Partner filters** (domain-based rules)
5. Save the record

Frontend visibility automatically adjusts based on the current user's
`res.partner` record:
* Hidden courses are not listed, searchable, or accessible.
* Courses with "Hide Join/Buy" mode remain visible but display an
  information message instead of enrollment options.

Technical details
=================

* Extends `slide.channel` with partner-domain fields and computed visibility logic  
* Inherits from `WebsiteSlides` controller to filter visible courses and hide CTAs  
* Filters search results and course listings dynamically  
* Includes XML view and QWeb template extensions


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
