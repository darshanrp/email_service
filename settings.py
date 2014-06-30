import logging.config

SERVER_PORT=8081
TIMEZONE='US/Eastern'

DEBUG=False

EMAIL_PROVIDER='MAILGUN'
URL='https://api.mailgun.net/v2/<MAILGUN_DOMAIN>/messages'
API_KEY=''

AUTO_SWITCH_EMAIL_PROVIDER=True

ALT_EMAIL_PROVIDER='MANDRILL'
ALT_URL='https://mandrillapp.com/api/1.0/messages/send.json'
ALT_API_KEY=''

LOGGING = {
	'version': 1,
	'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
	'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
	'loggers': {
        '__main__': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

logging.config.dictConfig(LOGGING)