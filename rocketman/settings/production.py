from .base import *

DEBUG = False
SECRET_KEY = 'zz17au+n5(tve(!0cjqf9*(d_ab)ald%gi7$$)tn$5=7&fj!e+'
ALLOWED_HOST = ['localhost', '*']

DATABASES = {
    "default":{
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": 'rocketman',
        "USER": 'rocketman',
        "PASSWORD": 'password',
        "HOST": 'localhost',
        "PORT": '',
    }
}
try:
    from .local import *
except ImportError:
    pass
