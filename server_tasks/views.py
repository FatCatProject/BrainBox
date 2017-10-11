from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import server_tasks.send as send_tasks


@login_required(login_url='login')
def external_trigger_put_foodboxes(request):
	send_tasks.put_foodboxes()
	return HttpResponse("external_trigger_put_foodboxes")


@login_required(login_url='login')
def external_trigger_put_feeding_logs(request):
	send_tasks.put_feedinglogs()
	return HttpResponse("external_trigger_put_feeding_logs")


def external_trigger_check_server_connection(request):
	connection_status = send_tasks.head_check_server_connection()
	return JsonResponse({"connection_status": connection_status})
