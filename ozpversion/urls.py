from django.conf.urls import url
from . import views

# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^$', views.version)
]
