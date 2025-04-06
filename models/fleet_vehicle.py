import requests

from odoo import models, fields
from odoo.exceptions import ValidationError

sync_fields = {'license_plate', 'tracking_device_sn'}

def odoo_to_traccar(device, vals):
    if 'license_plate' in vals:
        device['name'] = vals['license_plate']
    if 'tracking_device_sn' in vals:
        device['uniqueId'] = vals['tracking_device_sn']


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    tracking_device_sn = fields.Char(
        help="Tracking device serial number (Frotaweb subscription required)."
    )
    traccar_device_id = fields.Integer()

    def write(self, vals):
        if any(field in vals for field in sync_fields):
            base_url = self.env['ir.config_parameter'].sudo().get_param(
                'fleet_traccar.api_base_url') or 'http://gps.frotaweb.com/api'
            session = self.env['fleet_traccar.session'].sudo().search([('user_id', '=', self.env.user.id)], limit=1)
            if session:
                cookies = {'JSESSIONID': session.cookie}
                for record in self:
                    response = requests.get(f"{base_url}/devices/{record.traccar_device_id}", cookies=cookies)
                    device = response.json()
                    odoo_to_traccar(device, vals)
                    response = requests.put(f"{base_url}/devices/{record.traccar_device_id}", json=device, cookies=cookies)
                    if response.status_code != 200:
                        raise ValidationError(response.text)
            else:
                raise ValidationError("Unknown error")
        return super(FleetVehicle, self).write(vals)
