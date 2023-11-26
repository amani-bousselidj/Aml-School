class GeneralSettings:
    def __init__(self):
        self.site_name = "Your Site Name"
        self.phone = "123-456-7890"
        self.email = "example@example.com"
        self.facebook = "https://facebook.com/yourpage"
        self.twitter = "https://twitter.com/yourpage"
        # Add other settings here

    def update_settings(self, data):
        # Update settings from form data or other sources
        self.site_name = data.get('site_name', self.site_name)
        self.phone = data.get('phone', self.phone)
        self.email = data.get('email', self.email)
        # Update other settings

# Initialize the settings object
general_settings = GeneralSettings()
from django.apps import apps

def get_dynamic_site_logo(context):
    try:
        # Use the Apps class to get the model dynamically
        GeneralSettings = apps.get_model('SchoolManage', 'GeneralSettings')
        general_settings = GeneralSettings.objects.first()

        if general_settings and general_settings.logo:
            return general_settings.logo.url
    except apps.exceptions.AppRegistryNotReady:
        # Handle the exception if apps are not ready
        pass

  
#
 # Default logo URL
  # Default logo URL
from django.conf import settings  # Add this import statement
# SITE_LOGO_URL = '/static/admin/img/about-image-02.png' 
  # Default logo URL
from SchoolManage.models import GeneralSettings
JAZZMIN_SETTINGS = {
    "language_chooser": True,
    "site_logo": get_dynamic_site_logo,  # Use the function to get the logo URL    "site_title": "Aml School",
     "related_modal_active": False,
    "custom_css": "/static/css/custom_admin.css",
     "search_model": ["SchoolManage.CustomUser","SchoolManage.Course"],
     "search_app":["SchoolManage"],
     "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", },

        # external url that opens in a new window (Permissions can be added)

        # model admin to link to (Permissions checked against model)
        {"model": "SchoolManage.CustomUser"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "SchoolManage"},
    ],
     "usermenu_links": [
      
        {"model": "CustomUser"}
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
        "related_modal_active": False,
    "site_title": "Aml School",
    "site_header": "Aml_School",
    "site_brand": "Aml School",
 "changeform_format": "single",
    #  "site_logo": settings.SITE_LOGO_URL,
    # "site_logo": "images/photo_2023-11-11_10-56-40.jpg",
                    "navigation_expanded": True,
    "copyright": "Aml School",
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
"hide_apps": ["Auth","authtoken"],
"show_models":["Role"],

 "show_sidebar": True,
    "navigation_expanded": False,
"icons": {
        "auth": "fas fa-users-cog",  # Icon for the authentication app
        "auth.user": "fas fa-user",   # Icon for the User model
        "auth.Group": "fas fa-users",  # Icon for the Group model
        "SchoolManage.Role": "fas fa-user-graduate",  # Icon for the Role model
        "SchoolManage.Countries": "fas fa-globe",  # Icon for the Countries model
        "SchoolManage.CustomUser": "fas fa-user",  # Icon for the CustomUser model
        "SchoolManage.Student": "fas fa-user-graduate",  # Icon for the Student model
        "SchoolManage.Parent": "fas fa-user-friends",  # Icon for the Parent model
        "SchoolManage.Teacher": "fas fa-chalkboard-teacher",  # Icon for the Teacher model
        "SchoolManage.CourseCategory": "fas fa-folder",  # Icon for the CourseCategory model
        "SchoolManage.Subject": "fas fa-book",  # Icon for the Subject model
        "SchoolManage.Lesson": "fas fa-file-alt",  # Icon for the Lesson model
        "SchoolManage.Quiz": "fas fa-question",  # Icon for the Quiz model
        "SchoolManage.Course": "fas fa-graduation-cap",  # Icon for the Course model
        "SchoolManage.VideoLesson": "fas fa-video",  # Icon for the VideoLesson model
        "SchoolManage.CourseSection": "fas fa-book-open",  # Icon for the CourseSection model
        "SchoolManage.LessonOrder": "fas fa-list-ol",  # Icon for the LessonOrder model
        "SchoolManage.Choice": "fas fa-list",  # Icon for the Choice model
        "SchoolManage.Question": "fas fa-question-circle",  # Icon for the Question model
        "SchoolManage.QuestionChoice": "fas fa-check-circle",  # Icon for the QuestionChoice model
        "SchoolManage.Syllabus": "fas fa-calendar-alt",  # Icon for the Syllabus model
        "SchoolManage.LiveMeeting": "fas fa-video",  # Icon for the LiveMeeting model
        "SchoolManage.Class": "fas fa-school",  # Icon for the Class model
        "SchoolManage.Section": "fas fa-cube",  # Icon for the Section model
        "SchoolManage.ExamResult": "fas fa-poll",  # Icon for the ExamResult model
        "SchoolManage.LessonPlan": "fas fa-file-alt",  # Icon for the LessonPlan model
        "SchoolManage.Homework": "fas fa-book-open",  # Icon for the Homework model
        "SchoolManage.SubmitedHomworks": "fas fa-upload",  # Icon for the SubmitedHomworks model
        "SchoolManage.OnlineExam": "fas fa-tasks",  # Icon for the OnlineExam model
        "SchoolManage.StudentAttempt": "fas fa-pencil-alt",  # Icon for the StudentAttempt model
        "SchoolManage.StudentAnswer": "fas fa-check",  # Icon for the StudentAnswer model
        "SchoolManage.StudentProgress": "fas fa-tasks",  # Icon for the StudentProgress model
        "SchoolManage.Certificate": "fas fa-certificate",  # Icon for the Certificate model
        "SchoolManage.Rating": "fas fa-star",  # Icon for the Rating model
        "SchoolManage.Order": "fas fa-shopping-cart",  # Icon for the Order model
        "SchoolManage.Payment": "fas fa-money-check",  # Icon for the Payment model
        "SchoolManage.ShoppingCart": "fas fa-shopping-cart",  # Icon for the ShoppingCart model
        "SchoolManage.GeneralSettings": "fas fa-cogs",  # Icon for the GeneralSettings model
    },
}

JAZZMIN_SETTINGS["show_ui_builder"] = True
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-indigo",
    "accent": "accent-primary",
    "navbar": "navbar-indigo navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-indigo",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}