from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
import time
from django.utils import timezone

from .models import FeedingLog, Account, SystemLog, SystemSetting, FoodBox

from bbox.bboxDB import BrainBoxDB


def get_feeding_log_by_id(request, id):
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


def get_not_synced_feeding_logs(request):
	db = BrainBoxDB()
	mylogs = db.get_not_synced_feeding_logs()
	return HttpResponse(mylogs)


def set_feeding_log_synced(request, id):
	db = BrainBoxDB()
	mylog = db.set_feeding_log_synced(id)
	return HttpResponse(mylog)


def set_feeding_log_not_synced(request, id):
	db = BrainBoxDB()
	mylog = db.set_feeding_log_not_synced(id)
	return HttpResponse(mylog)


def delete_synced_feeding_logs(request):
	db = BrainBoxDB()
	mylogs = db.delete_synced_feeding_logs()
	return HttpResponse(mylogs)

def add_feeding_log(request, myLog):
	db = BrainBoxDB()
	mylog = db.add_feeding_log(myLog)
	return HttpResponse(mylog)

def get_system_log_by_id(request, id):
	db = BrainBoxDB()
	mylog = db.get_system_log_by_id(logID=id)
	return HttpResponse(mylog)

def get_all_system_logs(request):
	db = BrainBoxDB()
	mylogs = db.get_all_system_logs()
	return HttpResponse(mylogs)

def add_system_log(request, myLog):
	db = BrainBoxDB()
	mylog = db.add_system_log(myLog)
	return HttpResponse(mylog)

def get_system_setting(request, setting):
	db = BrainBoxDB()
	mylog = db.get_system_setting(setting)
	return HttpResponse(mylog)

def set_system_setting(request, setting, val):
	db = BrainBoxDB()
	mylog = db.set_system_setting(setting, val)
	return HttpResponse(mylog)


def get_account_info(request):
	db = BrainBoxDB()
	myAccount = db.get_account_info()
	return HttpResponse(myAccount)

def add_account(request, account):
	db = BrainBoxDB()
	mylog = db.add_account(account)
	return HttpResponse(mylog)

def change_user_name_and_or_password(request, acc, user_name, password):
	db = BrainBoxDB()
	mylog = db.change_user_name_and_or_password(acc, user_name, password)
	return HttpResponse(mylog)


def get_all_foodBoxes(request):
	db = BrainBoxDB()
	mylogs = db.get_all_foodBoxes()
	return HttpResponse(mylogs)

def delete_foodBox(request, myBox):
	db = BrainBoxDB()
	mylogs = db.delete_foodBox(myBox)
	return HttpResponse(mylogs)

def get_foodBox_by_foodBox_id(request, id):
	db = BrainBoxDB()
	mylog = db.get_foodBox_by_foodBox_id(id)
	return HttpResponse(mylog)


def test(request: HttpRequest):
	myfunc = request.GET.get("func")
	db = BrainBoxDB()
	if myfunc == "allFeedingLogs":
		return allFeedingLogs(request)

	if myfunc == "get_feeding_log_by_id":
		return get_feeding_log_by_id(request, id='06d32ba16ba544d49718c9506030308e')

	if myfunc == "get_all_feeding_logs":
		return get_all_feeding_logs(request)

	if myfunc == "get_synced_feeding_logs":
		return get_synced_feeding_logs(request)

	if myfunc == "get_not_synced_feeding_logs":
		return get_not_synced_feeding_logs(request)

	if myfunc == "set_feeding_log_synced":
		return set_feeding_log_synced(request, id='06d32ba16ba544d49718c9506030308e')

	if myfunc == "set_feeding_log_not_synced":
		return set_feeding_log_not_synced(request, id='06d32ba16ba544d49718c9506030308e')

	if myfunc == "delete_synced_feeding_logs":
		return delete_synced_feeding_logs(request)

	if myfunc == "add_feeding_log":
		box_id = FoodBox.objects.get(pk=2)
		myLog = FeedingLog(box_id=box_id,
								  feeding_id='2a27f997dc8f47499623d125f1f4b4df',
								  card_id='138-236-209-167-000',
								  open_time=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(1503402679)),
								  close_time=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(1503402679)),
								  start_weight='3',
								  end_weight='3',
								  synced= False)
		return add_feeding_log(request, myLog)

	if myfunc == "get_system_log_by_id":
		return get_system_log_by_id(request, id=1)

	if myfunc == "get_all_system_logs":
		return get_all_system_logs(request)

	if myfunc == "add_system_log":
		myLog = SystemLog(time_stamp=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(1503402679)),
								 message='msgNew',
								 message_type='Information',
								 severity=3)
		return add_system_log(request, myLog)

	if myfunc == "get_system_setting":
		setting = "BrainBox_Name"
		return get_system_setting(request, setting)

	if myfunc == "set_system_setting":
		setting = "BrainBox_ID"
		val = '111'
		return set_system_setting(request, setting, val)

	if myfunc == "get_account_info":
		return get_account_info(request)

	if myfunc == "add_account":
		acc = Account(user_name='Kot',password='Kot')
		return add_account(request, acc)

	if myfunc == "change_user_name_and_or_password":
		user_name = 'kottt'
		password = 'kottt'
		acc=Account.objects.get(user_name='kot')
		db.change_user_name_and_or_password(acc, user_name, password)
		return HttpResponse("Changed")

	if myfunc == "get_all_foodBoxes":
		return get_all_foodBoxes(request)

	if myfunc == "delete_foodBox":
		myBox = FoodBox.objects.get(box_id='3')
		return delete_foodBox(request,myBox)

	if myfunc == "get_foodBox_by_foodBox_id":
		return get_foodBox_by_foodBox_id(request, id='1')

	return HttpResponse("Blank")
