from common.conf import conf

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'default': {
            'format': '[%(asctime)s %(levelname)s %(process)d %(thread)d]: %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d ]: %(message)s',
            'datefmt': '%a, %d %b %Y %H:%M:%S %z',
        },
        'simple': {
            'format': '[%(levelname)s] %(asctime)s - ]: %(message)s',
            'datefmt': '%a, %d %b %Y %H:%M:%S %z',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['require_debug_true'],
        },
        'default_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': conf.log_file or 'logs/website.log',
            'when': 'midnight',
            'formatter': 'default',
            'backupCount': 30,  # approx 1 month worth
            'encoding': 'utf-8',
        },
        'access': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': conf.web_access_log_file or 'logs/web_access.log',
            'when': 'midnight',
            'formatter': 'default',
            'backupCount': 30,
            'encoding': 'utf-8',
        },
        'excep': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': conf.web_excep_log_file or 'logs/web_excep.log',
            'when': 'midnight',
            'formatter': 'default',
            'backupCount': 30,
            'encoding': 'utf-8',
        },
        'warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': conf.web_warning_log_file or 'logs/web_warning.log',
            'when': 'midnight',
            'formatter': 'default',
            'backupCount': 30,
            'encoding': 'utf-8',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['default_file', 'excep', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'access': {
            'handlers': ['access'],
            'level': 'INFO',
            'propagate': False
        }
    },
    'root': {
        'handlers': ['default_file', 'excep', 'console', 'warning'],
        'level': 'INFO',
    },
}
