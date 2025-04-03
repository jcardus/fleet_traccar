{
    'name': 'Fleet GPS',
    'version': '18.0.1.0.0',
    "summary": """
        This module extends the Fleet module allowing gps tracking.""",
    'depends': ['fleet'],
    'data': [
        'views/views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'fleet_traccar/static/src/**/*',
        ],
    },
}
