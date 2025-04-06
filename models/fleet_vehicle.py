import requests

from odoo import models, fields
from odoo.exceptions import ValidationError


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    tracking_device_sn = fields.Char(
        help="Tracking device serial number (Frotaweb subscription required).",
        unique = True
    )
    def write(self, vals):
        if 'tracking_device_sn' in vals and vals['tracking_device_sn']:
            try:
                base_url = self.env['ir.config_parameter'].sudo().get_param(
                    'fleet_traccar.api_base_url') or 'http://gps.frotaweb.com/api'
                json = {
                    "name": self.license_plate,
                    "uniqueId": vals.get("tracking_device_sn"),
                }
                session = self.env['fleet_traccar.session'].sudo().search([('user_id', '=', self.env.user.id)], limit=1)
                if session:
                    response = requests.post(f"{base_url}/devices", json=json, cookies={'JSESSIONID': session.cookie})
                    if response.status_code != 200:
                        raise ValidationError(
                            f"Failed to create device: {response.text}")
                else:
                    raise ValidationError("Unknown error")

            except ValidationError as e:
                raise ValidationError(f"Error creating device: {e}")

        return super(FleetVehicle, self).write(vals)

