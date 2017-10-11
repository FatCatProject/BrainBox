from django.conf.urls import url
from . import views

urlpatterns = [
	url(
		r'^external_trigger_put_foodboxes$',
		views.external_trigger_put_foodboxes,
		name='external_trigger_put_foodboxes'
	),
	url(
		r'^external_trigger_put_feeding_logs$',
		views.external_trigger_put_feeding_logs,
		name='external_trigger_put_feeding_logs'
	),
	url(
		r'^external_trigger_check_server_connection$',
		views.external_trigger_check_server_connection,
		name='external_trigger_check_server_connection'
	),
]
