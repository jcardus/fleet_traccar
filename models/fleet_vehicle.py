from odoo import models, fields


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    tracking_device_sn = fields.Char(
        help="Tracking device serial number (Frotaweb subscription required)."
    )