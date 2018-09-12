import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCATIONS = os.path.join(BASE_DIR, 'conf/locations.json')

WORKFLOW_URL = {
    'theme': 'http',
    'host': '52.80.138.64',
    'port': '30129',
    'root': 'jzActiviti',
}

CONNECTION = {
    'jzdbtest': {
        'theme': 'mysql+pymysql',
        'host': 'jzdbtest.crvo2o91g05z.rds.cn-north-1.amazonaws.com.cn',
        'port': '13306',
        'user': 'jzuser',
        'password': 'jz3205/*-',
        'database': 'jzdbtest',
    },
    'sso': {
        'theme': 'mysql+pymysql',
        'host': 'jzdbtest.crvo2o91g05z.rds.cn-north-1.amazonaws.com.cn',
        'port': '13306',
        'user': 'jzuser',
        'password': 'jz3205/*-',
        'database': 'sso',
    }
}

LOGGINGS = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'filename': os.path.join(BASE_DIR, 'log/logging.log'),
            'encoding': 'utf8',
            'maxBytes': 10485760,
            'backupCount': 10,
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'data': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
        'workflow': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
    }
}