from django.conf.urls import url
from . import views

#F_B

urlpatterns = [
    url(r'^/cancel/(?P<id>\d+)$', views.process_cancel_trip),
    url(r'^/join/(?P<id>\d+)$', views.process_join_trip),
    url(r'^/remove/(?P<id>\d+)$', views.process_remove_trip),
    url(r'^/edit_trip/(?P<id>\d+)$', views.process_edit_trip),
    url(r'^/edit/(?P<id>\d+)$', views.show_edit_trip),
    url(r'^/create_trip$', views.process_create_trip),
    url(r'^/new$', views.show_create_trip),
    url(r'^/(?P<id>\d+)$', views.show_trip),
    url(r'^$', views.dashboard),
]