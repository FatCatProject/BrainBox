from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^pushlogs/$', views.pushlogs, name="pushlogs"),
	url(r'^pullcards/(?P<box_id>[a-z0-9]{32})/$', views.pullcards, name="pullcards"),
	url(r'^pullfoodbox/(?P<box_id>[a-z0-9]{32})/$', views.pullfoodbox, name="pullfoodbox")
]
