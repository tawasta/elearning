from odoo import api, fields, models


class SlideChannelPartner(models.Model):
    _inherit = "slide.channel.partner"

    joined_date = fields.Datetime(
        string="Joined On",
        readonly=True,
        copy=False,
        help="Start of the current access period: when the participant joined "
        "or rejoined the course.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.setdefault("joined_date", fields.Datetime.now())
        return super().create(vals_list)

    def write(self, vals):
        """
        An invited participant who enrolls joins only now: start the access
        period from the enrollment, not from the invitation
        """
        joining_memberships = self.browse()
        if vals.get("member_status") not in (None, "invited"):
            joining_memberships = self.filtered(
                lambda membership: membership.member_status == "invited"
            )
        res = super().write(vals)
        if joining_memberships:
            joining_memberships.write({"joined_date": fields.Datetime.now()})
        return res

    def action_unarchive(self):
        """
        Rejoining a course (e.g. registering to another event linked to it)
        unarchives the old membership, which starts a new access period
        """
        rejoining_memberships = self.filtered(lambda membership: not membership.active)
        res = super().action_unarchive()
        rejoining_memberships.write({"joined_date": fields.Datetime.now()})
        return res
