"""
URL configuration for Schoolproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
# from SchoolManage.admin import show_permissions  # Import your actual view function

urlpatterns = [
        path("i18n/", include("django.conf.urls.i18n")),
    path('admin/', admin.site.urls),
        path("admin/", include('SchoolManage.urls')),
    path('api/',include('SchoolManage.urls')),
    # path('admin/show-permissions/<int:role_id>/', show_permissions, name='show_permissions'),
    # path('admin_tools_stats/', include('admin_tools_stats.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path

