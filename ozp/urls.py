"""ozp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from ozp.decorators.cas_decorators import redirecting_login_required

from decorator_include import decorator_include

urlpatterns = [
    url(r'^' + settings.OZP['ROOT_URL'] + 'admin/', include(admin.site.urls)),
    url(r'^' + settings.OZP['ROOT_URL'] + 'api/', decorator_include(redirecting_login_required, 'ozpcenter.urls')),
    url(r'^' + settings.OZP['ROOT_URL'] + 'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^' + settings.OZP['ROOT_URL'] + 'iwc-api/', include('ozpiwc.urls')),
    url(r'^' + settings.OZP['ROOT_URL'] + 'docs/', include('rest_framework_swagger.urls')),

    # CAS
    url(r'^' + settings.OZP['ROOT_URL'] + 'accounts/login/$', 'cas.views.login', name='login'),
    url(r'^' + settings.OZP['ROOT_URL'] + 'accounts/logout/$', 'cas.views.logout', name='logout'),
]

# in debug, serve the media and static resources with the django web server
# https://docs.djangoproject.com/en/1.8/howto/static-files/#serving-static-files-during-development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
