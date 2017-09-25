from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login$', views.login, name='login'),
	url(r'^register$', views.register, name='register'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^check_server_connection$', views.check_server_connection, name='check_server_connection'),
	url(r'^sync_box$', views.sync_box, name='sync_box'),
	url(r'^server_sync$', views.server_sync, name='server_sync')
]
