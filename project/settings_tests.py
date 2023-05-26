from .settings import *  # noqa

CELERY_TASK_ALWAYS_EAGER = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_test')

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}