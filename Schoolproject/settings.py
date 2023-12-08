"""
Django settings for Schoolproject project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vdzd+fpv9=*z83s)yox4h1(wpsomul!!^^xj$rl&a+50m*apk_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
CSRF_COOKIE_SAMESITE = 'Lax'
ALLOWED_HOSTS = ['aml-school.com', 'localhost', '0.0.0.0', '127.0.0.1']

CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:5173",
    'http://127.0.0.1',
    "https://aml-school.com"  # For production
]

CSRF_COOKIE_SECURE = True  # For development

CORS_ALLOW_CREDENTIALS = True  # For development; in production, specify your frontend's origin.

INSTALLED_APPS = [
    'jazzmin',
    #  'admin_tools_stats',  # this must be BEFORE 'admin_tools' and 'django.contrib.admin'
    # 'django_nvd3',

    #     'admin_tools',  # Include 'admin_tools' after 'admin_tools_stats'
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',

    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'SchoolManage',
    'rest_framework',
    'rest_framework.authtoken',
    'ckeditor',
    'corsheaders',
    # 'admin_interface',
    #    "admincharts",

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'SchoolManage.middleware.AdminLogoutMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar':        'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'Image', 'Link'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['Source'],
        ],
    }
}

ROOT_URLCONF = 'Schoolproject.urls'

TEMPLATES = [
    {
        'BACKEND':  'django.template.backends.django.DjangoTemplates',
        'DIRS':     [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS':  {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Schoolproject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':   BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar':        'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', 'Blockquote'],
            ['Link', 'Unlink', 'Anchor'],
            ['Source']
        ],
        'height':         300,
        'width':          600,
    },
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en', ('English')),
    ('ar', ('Arabic')),
    ('fr', ('French')),
]

TIME_ZONE = 'UTC'

USE_I18N = True
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]
USE_TZ = True

USE_I18N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Additional static file locations (if needed)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'Schoolproject/static')
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "SchoolManage.CustomUser"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',

    ],

}
# def get_dynamic_site_logo(context):
#     from SchoolManage.models import GeneralSettings  # Import inside the function

#     general_settings = GeneralSettings.objects.first()
#     if general_settings and general_settings.logo:
#         return general_settings.logo.url
#     return '/static/admin/img/about-image-02.png'  # Default logo URL
# from .admin_settings import get_dynamic_site_logo
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default ModelBackend
    # Add any custom backends if needed
]
# SITE_LOGO_URL = '/static/admin/img/about-image-02.png' 
# Default logo URL
JAZZMIN_SETTINGS = {
    "language_chooser":            True,
    # "site_logo": get_dynamic_site_logo,
    #  "site": "your_project_name.admin.custom_admin_site",  # Use the custom admin site
    "site_title":                  "Aml School",
    "related_modal_active":        False,
    "custom_css":                  "/static/css/custom_admin.css",
    "search_model":                ["SchoolManage.CustomUser", "SchoolManage.Course"],
    "search_app":                  ["SchoolManage"],
    "topmenu_links":               [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", },

        # external url that opens in a new window (Permissions can be added)

        # model admin to link to (Permissions checked against model)
        {"model": "SchoolManage.CustomUser"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "SchoolManage"},
    ],
    "usermenu_links":              [

        {"model": "CustomUser"}
    ],
    "show_sidebar":                True,
    "navigation_expanded":         True,
    "related_modal_active":        False,
    "site_title":                  "Aml School",
    "site_header":                 "Aml_School",
    "site_brand":                  "Aml School",
    "changeform_format":           "single",

    # "site_logo": "images/photo_2023-11-11_10-56-40.jpg",
    "navigation_expanded":         True,
    "copyright":                   "Aml School",
    "changeform_format":           "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    "hide_apps":                   ["Auth", "authtoken"],
    "show_models":                 ["Role"],

    "show_sidebar":                True,
    "navigation_expanded":         False,
    "icons":                       {
        "auth":                          "fas fa-users-cog",  # Icon for the authentication app
        "auth.user":                     "fas fa-user",  # Icon for the User model
        "auth.Group":                    "fas fa-users",  # Icon for the Group model
        "SchoolManage.Role":             "fas fa-user-graduate",  # Icon for the Role model
        "SchoolManage.Countries":        "fas fa-globe",  # Icon for the Countries model
        "SchoolManage.CustomUser":       "fas fa-user",  # Icon for the CustomUser model
        "SchoolManage.Student":          "fas fa-user-graduate",  # Icon for the Student model
        "SchoolManage.Parent":           "fas fa-user-friends",  # Icon for the Parent model
        "SchoolManage.Teacher":          "fas fa-chalkboard-teacher",  # Icon for the Teacher model
        "SchoolManage.CourseCategory":   "fas fa-folder",  # Icon for the CourseCategory model
        "SchoolManage.Subject":          "fas fa-book",  # Icon for the Subject model
        "SchoolManage.Lesson":           "fas fa-file-alt",  # Icon for the Lesson model
        "SchoolManage.Quiz":             "fas fa-question",  # Icon for the Quiz model
        "SchoolManage.Course":           "fas fa-graduation-cap",  # Icon for the Course model
        "SchoolManage.VideoLesson":      "fas fa-video",  # Icon for the VideoLesson model
        "SchoolManage.CourseSection":    "fas fa-book-open",  # Icon for the CourseSection model
        "SchoolManage.LessonOrder":      "fas fa-list-ol",  # Icon for the LessonOrder model
        "SchoolManage.Choice":           "fas fa-list",  # Icon for the Choice model
        "SchoolManage.Question":         "fas fa-question-circle",  # Icon for the Question model
        "SchoolManage.QuestionChoice":   "fas fa-check-circle",  # Icon for the QuestionChoice model
        "SchoolManage.Syllabus":         "fas fa-calendar-alt",  # Icon for the Syllabus model
        "SchoolManage.LiveMeeting":      "fas fa-video",  # Icon for the LiveMeeting model
        "SchoolManage.Class":            "fas fa-school",  # Icon for the Class model
        "SchoolManage.Section":          "fas fa-cube",  # Icon for the Section model
        "SchoolManage.ExamResult":       "fas fa-poll",  # Icon for the ExamResult model
        "SchoolManage.LessonPlan":       "fas fa-file-alt",  # Icon for the LessonPlan model
        "SchoolManage.Homework":         "fas fa-book-open",  # Icon for the Homework model
        "SchoolManage.SubmitedHomworks": "fas fa-upload",  # Icon for the SubmitedHomworks model
        "SchoolManage.OnlineExam":       "fas fa-tasks",  # Icon for the OnlineExam model
        "SchoolManage.StudentAttempt":   "fas fa-pencil-alt",  # Icon for the StudentAttempt model
        "SchoolManage.StudentAnswer":    "fas fa-check",  # Icon for the StudentAnswer model
        "SchoolManage.StudentProgress":  "fas fa-tasks",  # Icon for the StudentProgress model
        "SchoolManage.Certificate":      "fas fa-certificate",  # Icon for the Certificate model
        "SchoolManage.Rating":           "fas fa-star",  # Icon for the Rating model
        "SchoolManage.Order":            "fas fa-shopping-cart",  # Icon for the Order model
        "SchoolManage.Payment":          "fas fa-money-check",  # Icon for the Payment model
        "SchoolManage.ShoppingCart":     "fas fa-shopping-cart",  # Icon for the ShoppingCart model
        "SchoolManage.GeneralSettings":  "fas fa-cogs",  # Icon for the GeneralSettings model
    },
}

JAZZMIN_SETTINGS["show_ui_builder"] = True
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text":         False,
    "footer_small_text":         False,
    "body_small_text":           True,
    "brand_small_text":          False,
    "brand_colour":              "navbar-indigo",
    "accent":                    "accent-primary",
    "navbar":                    "navbar-indigo navbar-dark",
    "no_navbar_border":          False,
    "navbar_fixed":              False,
    "layout_boxed":              False,
    "footer_fixed":              True,
    "sidebar_fixed":             True,
    "sidebar":                   "sidebar-light-indigo",
    "sidebar_nav_small_text":    False,
    "sidebar_disable_expand":    False,
    "sidebar_nav_child_indent":  False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style":  False,
    "sidebar_nav_flat_style":    False,
    "theme":                     "default",
    "dark_mode_theme":           None,
    "button_classes":            {
        "primary":   "btn-primary",
        "secondary": "btn-secondary",
        "info":      "btn-info",
        "warning":   "btn-warning",
        "danger":    "btn-danger",
        "success":   "btn-success"
    }
}

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
