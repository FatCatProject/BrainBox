from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import server_tasks.send as send_tasks
import server_tasks.receive as receive_tasks


@login_required(login_url='login')
def external_trigger_put_foodboxes(request):
	send_tasks.put_foodboxes()
	return HttpResponse("external_trigger_put_foodboxes")


@login_required(login_url='login')
def external_trigger_put_feeding_logs(request):
	send_tasks.put_feedinglogs()
	return HttpResponse("external_trigger_put_feeding_logs")


@login_required(login_url='login')
def external_trigger_get_cards(request):
	receive_tasks.get_cards()
	return HttpResponse("external_trigger_get_cards")


@login_required(login_url='login')
def external_trigger_get_foodboxes(request):
	receive_tasks.get_foodboxes()
	return HttpResponse("external_trigger_get_foodboxes")


def external_trigger_check_server_connection(request):
	connection_status = send_tasks.head_check_server_connection()
	return JsonResponse({"connection_status": connection_status})

def external_trigger_server_sync(request):
	send_tasks.put_foodboxes()
	send_tasks.put_feedinglogs()
	receive_tasks.get_cards()
	receive_tasks.get_foodboxes()
	return HttpResponse(status=204)

