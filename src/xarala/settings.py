from django.contrib.messages import constants as messages
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "qliv-rs0nz3z0ccut(ie0$di0bm011-53y@q^u$^v9@kkpohpr"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # 3rd part apps
    "corsheaders",
    "graphene_django",
    "django_summernote",
    "crispy_forms",
    "celery",
    "embed_video",
    "import_export",
    # refresh tokens are optional
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
    "django_filters",
    # custom apps,
    "course.apps.CourseConfig",
    "pages.apps.PagesConfig",
    "users.apps.UsersConfig",
    "userlogs.apps.LogsConfig",
    "dashboard.apps.DashboardConfig",
    "blog.apps.BlogConfig",
    "search.apps.SearchConfig",
    "quiz.apps.QuizConfig",
    "podcast.apps.PodcastConfig",
    "order.apps.OrderConfig",
    "payment.apps.PaymentConfig",
    "cart.apps.CartConfig",
    "coupons.apps.CouponsConfig",
    "learning_path.apps.LearningPathConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

GRAPHENE = {
    "SCHEMA": "xarala.schema.schema",
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
}

GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_EXPIRATION_DELTA": timedelta(days=30),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=30),
    # optional
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
}


ROOT_URLCONF = "xarala.urls"
TEMPLATE_DIR = os.path.join(BASE_DIR, "xarala", "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cart.context_processors.cart",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]


WSGI_APPLICATION = "xarala.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
    "social_core.backends.github.GithubOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.twitter.TwitterOAuth",
    "social_core.backends.facebook.FacebookOAuth2",
    "django.contrib.auth.backends.ModelBackend",
]

SOCIAL_AUTH_FACEBOOK_KEY = ("1815308661957053",)
SOCIAL_AUTH_FACEBOOK_SECRET = ("c634b6ef2157ddf8ae5262f6c1dce23d",)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = (
    "223000822798-sv84dnbqhahq5bubmkta1tq95fa6i7rl.apps.googleusercontent.com",
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "YK_NOViediU9xeQkLScSSvIR"


SOCIAL_AUTH_GITHUB_KEY = "a changer"
SOCIAL_AUTH_GITHUB_SECRET = "a changer"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "profile"
LOGOUT_URL = "logout"
LOGOUT_REDIRECT_URL = "pages:home"
# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"


LANGUAGES = (
    ("en", _("English")),
    ("fr", _("French")),
)

PARLER_LANGUAGES = {
    None: (
        {"code": "en"},
        {"code": "fr"},
    ),
    "default": {
        "fallback": "en",
        "hide_untranslated": False,
    },
}

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "xarala/static")]
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


AUTH_USER_MODEL = "users.CustomUser"


# Messages
MESSAGE_TAGS = {messages.ERROR: "danger"}

CRISPY_TEMPLATE_PACK = "bootstrap4"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")


# django summernot
X_FRAME_OPTIONS = "SAMEORIGIN"
SUMMERNOTE_THEME = "bs4"
CRISPY_TEMPLATE_PACK = "bootstrap4"
# CELERY_BROKER_URL = "amqp://dbadmin:abc123!@127.0.0.1:5672//"
CELERY_BROKER_URL = "amqp://guest:guest@127.0.0.1:15672//"
CART_SESSION_ID = "cart"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale/"),)


REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 1


try:
    from .local_settings import *  # noqa
except ImportError:
    pass
