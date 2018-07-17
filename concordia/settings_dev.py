from .settings_template import *

LOGGING["handlers"]["stream"]["level"] = "DEBUG"
LOGGING["handlers"]["file"]["level"] = "DEBUG"
LOGGING["handlers"]["file"]["filename"] = "./logs/concordia-web.log"
LOGGING["handlers"]["celery"]["level"] = "DEBUG"
LOGGING["handlers"]["celery"]["filename"] = "./logs/concordia-celery.log"
LOGGING["loggers"]["django"]["level"] = "DEBUG"
LOGGING["loggers"]["celery"]["level"] = "DEBUG"

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "concordia",
        "USER": "concordia",
        "PASSWORD": "concordia",
        "HOST": "0.0.0.0",
        "PORT": "54321",
    }
}

ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0"]

CELERY_BROKER_URL = "amqp://"

CONCORDIA = {"netloc": "http://0.0.0.0:8000"}

IMPORTER = {
    "BASE_URL": "",
    "IMAGES_FOLDER": "/tmp/concordia_images/",
    "ITEM_COUNT": "",
    "S3_BUCKET_NAME": "",
}

AWS_ACCESS_KEY_ID = "AKIAJ2DPKGZ5E3SS3BOA"
AWS_SECRET_ACCESS_KEY = "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"
