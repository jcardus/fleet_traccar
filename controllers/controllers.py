# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

import requests


class ApiProxy(http.Controller):

    @http.route('/fleet_traccar/api/<path:_path>', type='http', auth='user')
    def proxy_request(self, _path):
        base_url = request.env['ir.config_parameter'].sudo().get_param(
            'fleet_traccar.api_base_url') or 'http://gps.frotaweb.com/api'
        response = requests.request(
            method=request.httprequest.method,
            url=f"{base_url.rstrip('/')}/{_path}?{request.httprequest.query_string.decode('utf-8')}",
            headers=dict(request.httprequest.headers),
            data=request.httprequest.data if request.httprequest.method in ['POST', 'PUT'] else None,
        )
        return request.make_response(response.content)
