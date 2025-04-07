from odoo import models, fields

class TraccarTrip(models.Model):
    _name = 'fleet_traccar.trip'
    _description = 'Trip Report'

    vehicle_id = fields.Many2one('fleet.vehicle', required=True)
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    distance = fields.Float()
    start_location = fields.Char()
    end_location = fields.Char()
    start_lat = fields.Float()
    start_lon = fields.Float()
    end_lat = fields.Float()
    end_lon = fields.Float()
