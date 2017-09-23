from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
import time
import datetime
from django.utils import timezone

from .models import FeedingLog, Account, SystemLog, SystemSetting, FoodBox

from bbox.bboxDB import BrainBoxDB


def get_feeding_log_by_id(request, id):
	mylog = BrainBoxDB.get_feeding_log_by_id(logID=id)
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
	mylogs = BrainBoxDB.get_all_feeding_logs()
	return HttpResponse(mylogs)


def get_synced_feeding_logs(request):
	mylogs = BrainBoxDB.get_synced_feeding_logs()
	return HttpResponse(mylogs)


def get_not_synced_feeding_logs(request):
	mylogs = BrainBoxDB.get_not_synced_feeding_logs()
	return HttpResponse(mylogs)


def set_feeding_log_synced(request, id):
	mylog = BrainBoxDB.set_feeding_log_synced(id)
	return HttpResponse(mylog)


def set_feeding_log_not_synced(request, id):
	mylog = BrainBoxDB.set_feeding_log_not_synced(id)
	return HttpResponse(mylog)


def delete_synced_feeding_logs(request):
	mylogs = BrainBoxDB.delete_synced_feeding_logs()
	return HttpResponse(mylogs)


def add_feeding_log(request, myLog):
	mylog = BrainBoxDB.add_feeding_log(myLog)
	return HttpResponse(mylog)


def get_system_log_by_id(request, id):
	mylog = BrainBoxDB.get_system_log_by_id(logID=id)
	return HttpResponse(mylog)


def get_all_system_logs(request):
	mylogs = BrainBoxDB.get_all_system_logs()
	return HttpResponse(mylogs)


def add_system_log(request, myLog):
	mylog = BrainBoxDB.add_system_log(myLog)
	return HttpResponse(mylog)


def get_system_setting(request, setting):
	mylog = BrainBoxDB.get_system_setting(setting)
	return HttpResponse(mylog)


def set_system_setting(request, setting, val):
	mylog = BrainBoxDB.set_system_setting(setting, val)
	return HttpResponse(mylog)


def get_account_info(request):
	myAccount = BrainBoxDB.get_account_info()
	return HttpResponse(myAccount)


def add_account(request, account):
	mylog = BrainBoxDB.add_account(account)
	return HttpResponse(mylog)


def change_user_name_and_or_password(request, acc, user_name, password):
	mylog = BrainBoxDB.change_user_name_and_or_password(acc, user_name, password)
	return HttpResponse(mylog)


def get_all_foodBoxes(request):
	mylogs = BrainBoxDB.get_all_foodBoxes()
	return HttpResponse(mylogs)


def delete_foodBox(request, myBox):
	mylogs = BrainBoxDB.delete_foodBox(myBox)
	return HttpResponse(mylogs)


def get_foodBox_by_foodBox_id(request, id):
	mylog = BrainBoxDB.get_foodBox_by_foodBox_id(id)
	return HttpResponse(mylog)


def test(request: HttpRequest):
	myfunc = request.GET.get("func")

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
		open_t = time.localtime(1503402679)  # type: time.struct_time
		close_t = time.localtime(1503402679)  # type: time.struct_time
		myLog = FeedingLog(
			box_id=box_id,
			feeding_id='2a27f997dc8f47499623d125f1f4b4df',
			card_id='138-236-209-167-000',
			open_time=datetime.datetime(
				open_t.tm_year, open_t.tm_mon, open_t.tm_mday, open_t.tm_hour, open_t.tm_min, open_t.tm_sec,
				tzinfo=datetime.timezone(offset=datetime.timedelta())  # This basically means "UTC == Local Time"

			),
			close_time=datetime.datetime(
				close_t.tm_year, close_t.tm_mon, close_t.tm_mday, close_t.tm_hour, close_t.tm_min, close_t.tm_sec,
				tzinfo=datetime.timezone(offset=datetime.timedelta())  # This basically means "UTC == Local Time"
			),
			start_weight='3',
			end_weight='3',
			synced=False
		)
		return add_feeding_log(request, myLog)

	if myfunc == "get_system_log_by_id":
		return get_system_log_by_id(request, id=1)

	if myfunc == "get_all_system_logs":
		return get_all_system_logs(request)

	if myfunc == "add_system_log":
		log_time = time.localtime(1503402679)  # type: time.struct_time
		print(log_time)
		myLog = SystemLog(
			time_stamp=datetime.datetime(
				log_time.tm_year, log_time.tm_mon, log_time.tm_mday, log_time.tm_hour, log_time.tm_min, log_time.tm_sec,
				tzinfo=datetime.timezone(offset=datetime.timedelta())  # This basically means "UTC == Local Time"
			),
			message='msgNew',
			message_type='Information',
			severity=3
		)
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
		# Why not just Account.objects.create(user_name='Kot', password='Kot') then?
		acc = Account(user_name='Kot', password='Kot')
		return add_account(request, acc)

	if myfunc == "change_user_name_and_or_password":
		user_name = 'kottt'
		password = 'kottt'
		acc = Account.objects.get(user_name='kot')
		BrainBoxDB.change_user_name_and_or_password(acc, user_name, password)
		return HttpResponse("Changed")

	if myfunc == "get_all_foodBoxes":
		return get_all_foodBoxes(request)

	if myfunc == "delete_foodBox":
		myBox = FoodBox.objects.get(box_id='3')
		return delete_foodBox(request, myBox)

	if myfunc == "get_foodBox_by_foodBox_id":
		return get_foodBox_by_foodBox_id(request, id='1')

	return HttpResponse("Blank")
