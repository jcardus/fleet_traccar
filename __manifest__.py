{
    'name': 'Frotaweb',
    'version': '18.0.1.0.1',
    "summary": """
        This module extends the Fleet module allowing gps tracking.""",
    'depends': ['fleet'],
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv'
    ],
    'assets': {
        'web.assets_backend': [
            'fleet_traccar/static/src/**/*',
        ],
    },
}
