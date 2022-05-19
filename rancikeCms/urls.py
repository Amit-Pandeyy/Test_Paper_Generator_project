"""rancikeCms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from main.sitemaps import StaticViewSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps={
    'static':StaticViewSitemap,
}

urlpatterns = [
    path('sitemap.xml/' , sitemap , {'sitemaps':sitemaps}, name='sitemap'),
    path('admin/', admin.site.urls),
    path('',include('main.urls')),
    path('',include('orders.urls')),
    path('',include('TeacherDashboard.urls')),
    path('accounts/', include('register_login.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('',include('questions.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('school_dashboard/', include('SchoolDashboard.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Edu Learning Admin"
admin.site.site_title = "Edu Learning Admin Portal"
admin.site.index_title = "Welcome to Edu Learning Admin Portal"