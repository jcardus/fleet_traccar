# -*- coding: utf-8 -*-
from http.cookies import SimpleCookie

from odoo import http
from odoo.exceptions import UserError
from odoo.http import request, Response

import requests
import uuid

class FleeTraccarController(http.Controller):

    def get_base_url(self):
        return request.env['ir.config_parameter'].sudo().get_param(
            'fleet_traccar.api_base_url') or 'http://gps.frotaweb.com/api'

    @http.route('/fleet_traccar/api/<path:_path>', type='http', auth='user', csrf=False)
    def proxy_request(self, _path):
        base_url = self.get_base_url()

        if request.httprequest.method in ['POST', 'PUT']:
            if 'application/x-www-form-urlencoded' in request.httprequest.headers.get('Content-Type', ''):
                body = dict(request.httprequest.form)
            else:
                body = request.httprequest.data
        else:
            body = None

        response = requests.request(
            method=request.httprequest.method,
            url=f"{base_url.rstrip('/')}/{_path}?{request.httprequest.query_string.decode('utf-8')}",
            headers=dict(request.httprequest.headers),
            data=body,
        )
        headers = dict()
        if 'Set-Cookie' in response.headers:
            headers['Set-Cookie'] = response.headers['Set-Cookie']
            cookie = SimpleCookie(response.headers['Set-Cookie'])
            session = request.env['fleet_traccar.session'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
            if session:
                session.write({'cookie': cookie.get('JSESSIONID').value})
            else:
                request.env['fleet_traccar.session'].sudo().create({
                    'user_id': request.env.user.id,
                    'cookie': cookie,
                })

        return request.make_response(response.content, status=response.status_code, headers=headers)

    @http.route('/fleet_traccar/instance_id', type='json')
    def get_instance_id(self):
        unique_id = 'fleet_traccar.unique_id'
        instance_id = request.env['ir.config_parameter'].get_param(unique_id)
        if not instance_id:
            instance_id = str(uuid.uuid4())  # Generate a unique UUID
            request.env['ir.config_parameter'].set_param(unique_id, instance_id)
        return instance_id

    @http.route('/fleet_traccar/add_devices', auth='user', type='json')
    def add_devices(self):
        base_url = self.get_base_url()
        cookie = request.httprequest.headers.get('Cookie')

        response = requests.get(
            f"{base_url.rstrip('/')}/devices", headers={'Cookie': cookie})

        if response.ok and len(response.json()) == 0:
            vehicles = request.env['fleet.vehicle'].sudo().search([])
            created = []

            for vehicle in vehicles:
                unique_id = str(uuid.uuid4())
                device_data = {
                    "name": vehicle.license_plate,
                    "uniqueId": unique_id,
                    "attributes": {
                        "odoo_vehicle_id": vehicle.id
                    }
                }

                response = requests.post(
                    f"{base_url.rstrip('/')}/devices",
                    json=device_data,
                    headers={
                        'Cookie': cookie
                    }
                )

                if not response.ok:
                    raise UserError(f"Failed to add device for {vehicle.name}: {response.text}")
                device = response.json()
                vehicle.sudo().write({'traccar_device_id': device['id']})
                created.append(vehicle.id)
            return {'added': created}
        raise UserError(response.text)

    @http.route('/fleet_traccar/contacts_kml', auth='user', type='http')
    def contacts_kml(self):
        partners = request.env['res.partner'].search([
            ('partner_latitude', '!=', False),
            ('partner_longitude', '!=', False)
        ])
        placemarks = ""
        for partner in partners:
            placemarks += f"""
                    <Placemark>
                        <name>{partner.name}</name>
                        <Point>
                            <coordinates>{partner.partner_longitude},{partner.partner_latitude},0</coordinates>
                        </Point>
                    </Placemark>
                    """
        kml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
                <kml xmlns="http://www.opengis.net/kml/2.2">
                  <Document>
                    <name>Contacts</name>
                    {placemarks}
                  </Document>
                </kml>"""
        return Response(kml_data)
