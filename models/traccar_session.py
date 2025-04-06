from odoo import models, fields

class TraccarSession(models.Model):
    _name = 'fleet_traccar.session'
    _description = 'Traccar Session Information'

    user_id = fields.Many2one('res.users', string="User", required=True)
    cookie = fields.Text(string="Session cookie", required=True)