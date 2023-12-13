from odoo import fields, models


class SlideChannel(models.Model):
    _inherit = "slide.channel"

    batch_id = fields.Many2one(string="Batch", comodel_name="op.batch")


class SlideChannelPartner(models.Model):
    _inherit = "slide.channel.partner"

    def create(self, vals_list):
        records = super().create(vals_list)
        if records.channel_id.batch_id:
            vals = {
                "partner_id": records.partner_id.id,
                "first_name": records.partner_id.firstname,
                "last_name": records.partner_id.lastname,
                "email": records.partner_id.email,
                "mobile": records.partner_id.phone,
            }
            student_batch_vals = {
                "batch_id": records.channel_id.batch_id.id,
                "channel_id": records.channel_id.id,
            }
            is_student = (
                self.env["op.student"]
                .sudo()
                .search([("partner_id", "=", records.partner_id.id)])
            )
            if is_student:
                student_batch_vals.update({"student_id": is_student.id})
            else:
                create_student = self.env["op.student"].sudo().create(vals)
                student_batch_vals.update({"student_id": create_student.id})

            self.env["op.batch.students"].sudo().create(student_batch_vals)
        return records
