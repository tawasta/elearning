import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ChannelsReorderCategoriesWizard(models.TransientModel):

    _name = "channels.reorder.categories.wizard"

    category_ids = fields.One2many(
        comodel_name="channels.reorder.categories.wizard.category",
        inverse_name="reorder_wizard_id",
        string="Categories",
    )

    @api.model
    def default_get(self, fields):
        """
        When wizard launches, populate the category list with the course's current
        categories, in their current order.
        """

        channel_obj = self.env["slide.channel"]
        channel_id = self._context["active_id"]

        res = super().default_get(fields)

        category_ids = channel_obj.search([("id", "=", channel_id)]).slide_ids.filtered(
            lambda s: s.is_category
        )

        res["category_ids"] = [
            (
                0,
                0,
                {
                    # sequence modifiable by user in wizard
                    "sequence": category_id.sequence,
                    "original_sequence": category_id.sequence,
                    "original_id": category_id.id,
                    "original_name": category_id.name,
                },
            )
            for category_id in category_ids
        ]

        return res

    def confirm(self):
        """
        Apply the reordering by recalculating sequences for all of the channel's
        slides and categories
        """

        channel_obj = self.env["slide.channel"]
        slide_obj = self.env["slide.slide"]
        channel_id = self._context["active_id"]

        current_channel = channel_obj.search([("id", "=", channel_id)])

        # ID-sequence pairs for slides
        new_sequences = {}

        # running sequence number
        sequence_to_use = False

        # Check first for any category-less slides in the beginning and leave them
        # and their sequences they are
        for slide in current_channel.slide_ids:
            if slide.is_category:
                # Grab the first category's sequence to be used as a starting sequence
                sequence_to_use = slide.sequence
                break
            else:
                _logger.debug("Bypassing slide %s that has no category" % slide.name)

        # Iterate through the wizard's newly reordered categories one by one
        for reordered_category in self.category_ids:

            _logger.debug(
                "-- Assigning category '%s' sequence %s"
                % (reordered_category.original_name, sequence_to_use)
            )
            new_sequences[reordered_category.original_id] = sequence_to_use
            sequence_to_use += 1

            # Find all slides that are currently children of the category. Give them
            # sequence numbers just after the category's sequence.
            for slide in current_channel.slide_ids:
                if slide.sequence <= reordered_category.original_sequence:
                    # _logger.debug(
                    #     "Ignoring slide %s, belongs to earlier categories.",
                    #     slide.name
                    # )
                    continue

                if slide.is_category:
                    _logger.debug(
                        "-- Next category '%s' encountered, all slides found "
                        "for category '%s'."
                        % (slide.name, reordered_category.original_name)
                    )
                    break

                _logger.debug(
                    "-- Assigning slide '%s' sequence of %s"
                    % (slide.name, sequence_to_use)
                )
                new_sequences[slide.id] = sequence_to_use
                sequence_to_use += 1

        # Store the calculated new sequences
        slides_to_update = slide_obj.browse(new_sequences.keys())
        for slide in slides_to_update:
            slide.write({"sequence": new_sequences[slide.id]})
