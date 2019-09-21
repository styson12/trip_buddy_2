from django.conf.urls import url
from . import views

#L_R

urlpatterns = [
    url(r'^logout', views.logout),
    url(r'^process_login', views.process_login),
    url(r'^$', views.index),
]