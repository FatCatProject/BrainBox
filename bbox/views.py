from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest

from .models import FeedingLog, Account
from bbox.bboxDB import BrainBoxDB


def feedinglogbyid(request, id):
	db = BrainBoxDB()
	mylog = db.get_feeding_log_by_id(logID=id)
	return HttpResponse(mylog)

def allFeedingLogs(request):
	all_feeding_logs = FeedingLog.objects.all()
	output = ', '.join([FeedingLog.feeding_id for FeedingLog in all_feeding_logs])
	return HttpResponse(output)


def accounts(request):
	accounts = Account.objects.all()
	output = ', '.join([Account.user_name for Account in accounts])
	return HttpResponse(output)


def get_all_feeding_logs(request):
	db = BrainBoxDB()
	mylogs = db.get_all_feeding_logs()
	return HttpResponse(mylogs)

def get_synced_feeding_logs(request):
	db = BrainBoxDB()
	mylogs = db.get_synced_feeding_logs()
	return HttpResponse(mylogs)

def test(request: HttpRequest):
	myfunc = request.GET.get("func")

	if myfunc == "allFeedingLogs":
		return allFeedingLogs(request)

	if myfunc == "feedinglogbyid":
		return feedinglogbyid(request, id='2a27f997dc8f47499623d125f1f4b4df')

	if myfunc == "get_all_feeding_logs":
		return get_all_feeding_logs(request)

	if myfunc == "get_synced_feeding_logs":
		return get_synced_feeding_logs(request)

	return HttpResponse("Blank")
