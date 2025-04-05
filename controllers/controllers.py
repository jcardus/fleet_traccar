# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

import requests
import uuid

class FleeTraccarController(http.Controller):

    @http.route('/fleet_traccar/api/<path:_path>', type='http', auth='user', csrf=False)
    def proxy_request(self, _path):
        base_url = request.env['ir.config_parameter'].sudo().get_param(
            'fleet_traccar.api_base_url') or 'http://gps.frotaweb.com/api'

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

        return request.make_response(response.content, status=response.status_code, headers=headers)


    @http.route('/fleet_traccar/instance_id', type='json')
    def get_instance_id(self):
        unique_id = 'fleet_traccar.unique_id'
        instance_id = request.env['ir.config_parameter'].get_param(unique_id)
        if not instance_id:
            instance_id = str(uuid.uuid4())  # Generate a unique UUID
            request.env['ir.config_parameter'].set_param(unique_id, instance_id)
        return instance_id