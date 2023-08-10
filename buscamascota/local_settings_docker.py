import os

from buscamascota.settings import BASE_DIR

trusted_origins = os.environ.get("CSRF_TRUSTED_ORIGINS")
if trusted_origins is not None:
    CSRF_TRUSTED_ORIGINS = [x.strip() for x in trusted_origins.split(",")]

allowed_hosts = os.environ.get("ALLOWED_HOSTS")
if allowed_hosts is not None:
    ALLOWED_HOSTS = [x.strip() for x in allowed_hosts.split(",")]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = []
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}