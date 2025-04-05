# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

import requests


class ApiProxy(http.Controller):

    @http.route('/fleet_traccar/api/<path:_path>', type='http', auth='user')
    def proxy_request(self, _path):
        base_url = request.env['ir.config_parameter'].sudo().get_param(
            'fleet_traccar.api_base_url') or 'http://gps.frotaweb.com/api'

        if request.httprequest.method in ['POST', 'PUT']:
            if 'application/json' in request.httprequest.headers.get('Content-Type', ''):
                body = request.jsonrequest
            elif 'application/x-www-form-urlencoded' in request.httprequest.headers.get('Content-Type', ''):
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
        return request.make_response(response.content, status=response.status_code)
