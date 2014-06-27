import logging.config

EMAIL_PROVIDER='MAILGUN'
URL='https://api.mailgun.net/v2/sandbox331829865a9e46e7861445357c0d24ec.mailgun.org/messages'
API_KEY=''

AUTO_SELECT_EMAIL_PROVIDER=False

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