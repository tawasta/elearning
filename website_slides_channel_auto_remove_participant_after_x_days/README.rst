.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================================
eLearning: Auto-remove Course Participants after X Days
=======================================================

* Enables setting a day threshold after which participants' access 
  will be revoked.
* Intended for situations where you want to keep a course open 
  indefinitely, but each participant should e.g. only get a 30-day
  access to the course materials
  

Configuration
=============
* In the Course form view, set the new "Auto-remove Participant Access" field
  and the related day threshold field.
* Finetune the cron interval if needed. Default is every 24 hours.

Usage
=====
* Let users register to courses as usual. Their access will be revoked as 
  enough days pass from their initial course registration.

Known issues / Roadmap
======================
* If you need a course-wide archive date and have no need for participant-specific
  access revoking, see the website_slides_auto_archive_cron module instead.

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
