import base64
import logging
import re

import requests
from werkzeug import urls

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class Slide(models.Model):
    _inherit = "slide.slide"

    YOUTUBE_VIDEO_ID_REGEX = (
        r"^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*"
    )
    GOOGLE_DRIVE_DOCUMENT_ID_REGEX = (
        r"(^https:\/\/docs.google.com|^https:\/\/drive.google.com).*\/d\/([^\/]*)"
    )
    VIMEO_VIDEO_ID_REGEX = (
        r"\/\/(player.)?vimeo.com\/(?:[a-z]*\/)*([0-9]{6,11})\/?([0-9a-z]{6,11})?[?]?.*"
    )

    vimeo_id = fields.Char("Video Vimeo ID", compute="_compute_vimeo_id")
    video_source_type = fields.Selection(
        [("youtube", "YouTube"), ("google_drive", "Google Drive"), ("vimeo", "Vimeo")],
        string="Video Source",
        compute="_compute_video_source_type",
    )
    video_url = fields.Char(
        "Video Link",
        related="url",
        readonly=False,
        help="Link of the video (we support YouTube, Google Drive and Vimeo as sources)",
    )
    document_id_helper = fields.Text(
        "Embed code helper", compute="_compute_document_id_helper"
    )

    embed_code_external = fields.Html(
        "External Embed Code",
        readonly=True,
        compute="_compute_embed_code",
        sanitize=False,
        help="Same as 'Embed Code' but used to embed the content on an external website.",
    )

    @api.depends("url")
    def _compute_video_source_type(self):
        for slide in self:
            video_source_type = False
            youtube_match = (
                re.match(self.YOUTUBE_VIDEO_ID_REGEX, slide.video_url)
                if slide.video_url
                else False
            )
            if (
                youtube_match
                and len(youtube_match.groups()) == 2
                and len(youtube_match.group(2)) == 11
            ):
                video_source_type = "youtube"
            if (
                slide.video_url
                and not video_source_type
                and re.match(self.GOOGLE_DRIVE_DOCUMENT_ID_REGEX, slide.video_url)
            ):
                video_source_type = "google_drive"
            vimeo_match = (
                re.search(self.VIMEO_VIDEO_ID_REGEX, slide.video_url)
                if slide.video_url
                else False
            )
            if not video_source_type and vimeo_match and len(vimeo_match.groups()) == 3:
                video_source_type = "vimeo"

            slide.video_source_type = video_source_type

    @api.depends(
        "document_id", "slide_type", "mime_type", "vimeo_id", "video_source_type"
    )
    def _compute_embed_code(self):
        res = super()._compute_embed_code()

        for slide in self:
            if slide.video_source_type == "vimeo":
                embed_code_external = False

                if "/" in slide.vimeo_id:
                    # in case of privacy 'with URL only', vimeo adds a token after the video ID
                    # the embed url needs to receive that token as a "h" parameter
                    [vimeo_id, vimeo_token] = slide.vimeo_id.split("/")

                    # flake8: noqa: C901
                    embed_code = """
                    <iframe src="https://player.vimeo.com/video/%s?h=%s&badge=0&amp;autopause=0&amp;player_id=0"
                    frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen>
                    </iframe>""" % (
                        vimeo_id,
                        vimeo_token,
                    )
                else:
                    # flake8: noqa: C901
                    embed_code = """
                    <iframe src="https://player.vimeo.com/video/%s?badge=0&amp;autopause=0&amp;player_id=0"
                    frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen>
                    </iframe>""" % (
                        slide.vimeo_id
                    )

                slide.embed_code = embed_code
                slide.embed_code_external = embed_code_external or embed_code

            return res

    @api.onchange("url", "slide_type")
    @api.depends("url", "slide_type")
    def _compute_vimeo_id(self):
        for slide in self:
            if slide.url and slide.video_source_type == "vimeo":
                match = re.search(self.VIMEO_VIDEO_ID_REGEX, slide.url)
                if match and len(match.groups()) == 3:
                    if match.group(3):
                        # in case of privacy 'with URL only',
                        # vimeo adds a token after the video ID
                        # the share url is then 'vimeo_id/token'
                        # the token will be captured in the third group of the regex (if any)
                        vimeo_id = "%s/%s" % (match.group(2), match.group(3))
                        slide.vimeo_id = vimeo_id
                        slide.document_id = vimeo_id

                    else:
                        # regular video, we just capture the vimeo_id
                        vimeo_id = match.group(2)
                        slide.vimeo_id = vimeo_id
                        slide.document_id = vimeo_id
            else:
                slide.vimeo_id = False
                slide.document_id = False

    @api.onchange("url", "video_url")
    def _on_change_url(self):
        """Keeping a 'onchange' because we want this behavior for the frontend.
        Changing the document / video external URL will populate some metadata on the form view.
        We only populate the field that are empty to avoid overriding user assigned values.
        The slide metadata are also fetched in create / write
        overrides to ensure consistency."""

        self.ensure_one()
        if self.url or self.video_url:
            slide_metadata, _error = self._fetch_external_metadata()
            if slide_metadata:
                self.update(
                    {
                        key: value
                        for key, value in slide_metadata.items()
                        if not self[key]
                    }
                )

    def _fetch_external_metadata(self, image_url_only=False):
        self.ensure_one()

        slide_metadata = {}
        error = False
        if self.slide_type == "video" and self.video_source_type == "vimeo":
            slide_metadata, error = self._fetch_vimeo_metadata(image_url_only)

        return slide_metadata, error

    def _fetch_vimeo_metadata(self, image_url_only=False):
        """Fetches video metadata from the Vimeo API.
        See https://developer.vimeo.com/api/oembed/showcases for more information.

        Returns a dict containing video metadata with the following keys
        (matching slide.slide fields):
        - 'name' matching the video title
        - 'description' matching the video description
        - 'image_1920' binary data of the video thumbnail
          OR 'image_url' containing an external link to the thumbnail
          when 'fetch_image' param is False
        - 'completion_time' matching the video duration

        :param image_url_only: if False, will return 'image_url' instead of binary data
          Typically used when displaying a slide preview to the end user.
        :return a tuple (values, error) containing the values of the slide and a potential error
          (e.g: 'Video could not be found')"""

        self.ensure_one()
        error_message = False
        try:
            response = requests.get(
                "https://vimeo.com/api/oembed.json?%s"
                % urls.url_encode({"url": self.video_url}),
                timeout=3,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            error_message = e.response.content
            if e.response.status_code == 404:
                return {}, _(
                    "Your video could not be found on Vimeo, "
                    "please check the link and/or privacy settings"
                )
        except requests.exceptions.ConnectionError as e:
            error_message = str(e)

        if not error_message and "application/json" in response.headers.get(
            "content-type"
        ):
            response = response.json()
            if response.get("error"):
                error_message = (
                    response.get("error", {}).get("errors", [{}])[0].get("reason")
                )

            if not response:
                error_message = _("Please enter a valid Vimeo video link")

        if error_message:
            _logger.warning("Could not fetch Vimeo metadata: %s", error_message)
            return {}, error_message

        vimeo_values = response
        slide_metadata = {"slide_type": "video"}

        if vimeo_values.get("title"):
            slide_metadata["name"] = vimeo_values.get("title")

        if vimeo_values.get("description"):
            slide_metadata["description"] = vimeo_values.get("description")

        if vimeo_values.get("duration"):
            # seconds to hours conversion
            slide_metadata["completion_time"] = (
                round(vimeo_values.get("duration") / 60) / 60
            )

        thumbnail_url = vimeo_values.get("thumbnail_url")
        if thumbnail_url:
            if image_url_only:
                slide_metadata["image_url"] = thumbnail_url
            else:
                slide_metadata["image_1920"] = base64.b64encode(
                    requests.get(thumbnail_url, timeout=3).content
                )

        return slide_metadata, None
