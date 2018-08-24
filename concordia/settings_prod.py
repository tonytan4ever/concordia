import os
from .settings_template import *

LOGGING["handlers"]["stream"]["level"] = "INFO"
LOGGING["handlers"]["file"]["level"] = "INFO"
LOGGING["handlers"]["file"]["filename"] = "./logs/concordia-web.log"
LOGGING["handlers"]["celery"]["level"] = "INFO"
LOGGING["handlers"]["celery"]["filename"] = "./logs/concordia-celery.log"
LOGGING["loggers"]["django"]["level"] = "INFO"
LOGGING["loggers"]["celery"]["level"] = "INFO"

DJANGO_SECRET_KEY = "changeme"

# TODO: For final deployment to production,
# when we are running https, uncomment this next line
# CSRF_COOKIE_SECURE = True

IMPORTER = {
    "BASE_URL": "",
    # /concordia_images is a docker volume shared by importer and concordia
    "IMAGES_FOLDER": "/concordia_images/",
    "ITEM_COUNT": "",
    "S3_BUCKET_NAME": "",
}

EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "")
DEFAULT_TO_EMAIL = DEFAULT_FROM_EMAIL

# HMAC activation flow provide the two-step registration process,
# the user signs up and then completes activation via email instructions.
REGISTRATION_URLS = "registration.backends.hmac.urls"
REGISTRATION_SALT = "registration"  # doesn't need to be secret

ACCOUNT_ACTIVATION_DAYS = 1  # required for HMAC registration two-step-flow
