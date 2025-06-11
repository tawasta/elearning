.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================
Website Slides Dynamic Progression
==================================

This module extends the `website_slides` (eLearning) module by allowing slides (lessons) to be locked behind prerequisites. A slide can define which other slides must be completed before the user is allowed to view or access it.

Features
============

* Add "Required Previous Slides" field to each slide.
* Prevent access to slides unless the user has completed the required previous slides.
* Update slide UI dynamically after quiz or slide completion (no full page reload needed).
* Lock visual representation for inaccessible slides (with lock icon and warning).
* Integrated into:
  * Slide list view.
  * Slide fullscreen sidebar.
  * Slide detailed content.
  * Training aside list.

Configuration
=============

No specific configuration is needed.

However, to define dependencies:
1. Go to **eLearning / Courses**.
2. Open a course and edit a slide.
3. Use the new field **"Required Previous Slides"** to select slides that must be completed beforehand.

Usage
=====

When a user views a course:

* Only slides with all prerequisites completed are clickable.
* Inaccessible slides:
  * Show greyed-out names.
  * Display a list of missing prerequisites.

The slide list and UI are dynamically updated after each slide or quiz completion to reflect progress, using JavaScript enhancements.


Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
