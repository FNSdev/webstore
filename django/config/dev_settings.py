from config.common_settings import *

DEBUG = True
SECRET_KEY = 'webstore'

DATABASES['default'].update({
    'NAME': 'webstore',
    'USER': 'webstore',
    'PASSWORD': 'development',
    'HOST': 'locahost',
    'PORT': '5432',
})

MEDIA_ROOT = os.path.join(BASE_DIR, '../media_root')

