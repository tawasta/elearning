.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================
Website Slides Certification Delay
==================================

This module adds control over the retry timing for failed course certifications
in Odoo eLearning (Slides). Administrators can define a delay (in hours) before
a user can retry a failed certification quiz.

Key Features
============

- New field `Retry Delay (hours)` for each Slide Channel to configure delay between failed attempts.
- Tracks user's last failed attempt time and calculates when they can try again.
- Retry button in survey is automatically hidden until retry is allowed.
- Informative message shown to the user when retry becomes available.

Configuration
=============

1. Go to *eLearning > Courses* and open a course (Slide Channel).
2. Set the value of **Retry Delay (hours)** under the Website field.
3. Save the course.

Usage
=====

- When a user fails a certification survey and has no more allowed attempts:
  - Their `last_failed_attempt` and `next_retry_possible_at` are set.
  - The retry button will be hidden until the retry delay has passed.
  - A message is shown indicating when they can try again.

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
