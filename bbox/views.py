from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
import time
import datetime
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt

from .models import FeedingLog, Account, SystemLog, SystemSetting, FoodBox, Card

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


def add_account(request, user, passwod):
	mylog = BrainBoxDB.add_account(user, passwod)
	return HttpResponse()


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


def get_all_cards(request):
	cards = BrainBoxDB.get_all_cards()
	return HttpResponse(cards)


def get_cards(request, isadmin):
	cards = BrainBoxDB.get_cards(isadmin)
	return HttpResponse(cards)


def get_boxes_for_card(request, cardID):
	boxes = BrainBoxDB.get_boxes_for_card(cardID)
	return HttpResponse(boxes)


def get_cards_for_box(request, boxID):
	boxes = BrainBoxDB.get_cards_for_box(boxID)
	return HttpResponse(boxes)


def set_card_name(request, id, newName):
	card = BrainBoxDB.set_card_name(id, newName)
	return HttpResponse(card)


def get_card_by_name(request, name):
	card = BrainBoxDB.get_card_by_name(name)
	return HttpResponse(card)


def add_card(request, card_id, card_name):
	card = BrainBoxDB.add_card(card_id, card_name)
	return HttpResponse(card)


def set_card_active_for_box(request, card_id, box_id):
	card = BrainBoxDB.set_card_active_for_box(card_id, box_id)
	return HttpResponse(card)


def set_card_not_active_for_box(request, card_id, box_id):
	card = BrainBoxDB.set_card_not_active_for_box(card_id, box_id)
	return HttpResponse(card)


def associate_card_with_box(request, card_id, box_id):
	cardOpen = BrainBoxDB.associate_card_with_box(card_id, box_id)
	return HttpResponse(cardOpen)


def delete_card(request, card_id):
	card = BrainBoxDB.delete_card(card_id)
	return HttpResponse(card)


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
		myLog = FeedingLog(
			box_id=box_id,
			feeding_id='2a27f997dc8f47499623d125f1f4b4df',
			card_id='138-236-209-167-000',
			open_time=1503402679,
			close_time=1503402679,
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
		myLog = SystemLog(
			time_stamp=1503402679,
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
		return add_account(request, 'a', 'a')

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

	if myfunc == "get_all_cards":
		return get_all_cards(request)

	if myfunc == "get_cards":
		isAdmin = False
		return get_cards(request, isAdmin)

	if myfunc == "get_boxes_for_card":
		card = '146-041-165-049-000'
		return get_boxes_for_card(request, card)

	if myfunc == "get_cards_for_box":
		boxId = '2'
		return get_cards_for_box(request, boxId)

	if myfunc == "set_card_name":
		boxId = '138-236-209-167-111'
		newName = 'Ellie'
		return set_card_name(request, boxId, newName)

	if myfunc == "get_card_by_name":
		card_name = 'Ellie'
		return get_card_by_name(request, card_name)

	if myfunc == "add_card":
		return add_card(request, '146-154-123-255-011', 'Chavka')

	if myfunc == "set_card_active_for_box":
		return set_card_active_for_box(request, '102-165-229-203-000', 1)

	if myfunc == "set_card_not_active_for_box":
		return set_card_not_active_for_box(request, '102-165-229-203-000', 1)

	if myfunc == "associate_card_with_box":
		card = Card.objects.get(card_id='102-165-229-203-000')
		box = FoodBox.objects.get(box_id=1)
		return associate_card_with_box(request, card, box)

	if myfunc == "delete_card":
		return delete_card(request, '138-236-209-167-001')

	return HttpResponse("Blank")


@csrf_exempt
def pushlogs(request):
	""" Add FeedingLogs to a specific FoodBox's log and confirm them in the response."""

	try:
		request_body = json.loads(request.body.decode("utf-8"))
		request_foodbox = BrainBoxDB.get_foodBox_by_foodBox_id(request_body["box_id"])  # type: FoodBox
		request_feedinglogs = request_body["feeding_logs"]
	except (ValueError, AttributeError) as e:
		my_log = SystemLog(
			time_stamp=time.time(),
			message="Unexpected request body: {0}".format(str(e.args)),
			message_type="Fatal",
			severity=2
		)
		print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
		BrainBoxDB.add_system_log(myLog=my_log)
		return HttpResponse(status=400)

	box_cards = {
		card.card_id: card for card in BrainBoxDB.get_cards_for_box(box_id=request_foodbox.box_id, active_only=False)
	}

	confirmed_ids = []
	for log in request_feedinglogs:
		tmp_feeding_id = log["feeding_id"]
		tmp_card_id = box_cards[log["card_id"]]
		tmp_open_time = log["open_time"]
		tmp_close_time = log["close_time"]
		tmp_start_weight = log["start_weight"]
		tmp_end_weight = log["end_weight"]
		tmp_feedinglog = FeedingLog(
			box_id=request_foodbox, feeding_id=tmp_feeding_id, card_id=tmp_card_id, open_time=tmp_open_time,
			close_time=tmp_close_time, start_weight=tmp_start_weight, end_weight=tmp_end_weight, synced=False
		)
		BrainBoxDB.add_feeding_log(tmp_feedinglog)
		confirmed_ids.append(tmp_feeding_id)

	request_foodbox.box_ip = request.META["REMOTE_ADDR"]
	now = time.localtime()
	now_datetime = datetime.datetime(
		now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec,
		tzinfo=datetime.timezone(offset=datetime.timedelta())
	)
	request_foodbox.box_last_sync = now_datetime
	request_foodbox.save()

	response_json = json.dumps({"confirm_ids": confirmed_ids})
	response = HttpResponse(content=response_json, content_type="application/json", status=200)

	my_log = SystemLog(
		time_stamp=time.time(),
		message="push_logs from FoodBox succeeded.",
		message_type="Information",
		severity=0
	)
	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	BrainBoxDB.add_system_log(myLog=my_log)
	return response


def pullcards(request, box_id):
	request_foodbox = BrainBoxDB.get_foodBox_by_foodBox_id(box_id)  # type: FoodBox
	cards_to_sync = BrainBoxDB.get_unsynced_cards_for_box(box_id=request_foodbox.box_id)
	# admin_cards = BrainBoxDB.get_cards(admin=True)

	cards_to_sync_list = [
		{
			"card_id": cardopen.card_id.card_id,
			"active": cardopen.active,
			"card_name": cardopen.card_id.card_name
		}
		for cardopen in cards_to_sync if not cardopen.card_id.admin
	]
	admin_cards_list = [
		{
			"card_id": cardopen.card_id.card_id,
			"active": cardopen.active,
			"card_name": "ADMIN"
		}
		for cardopen in cards_to_sync if cardopen.card_id.admin
	]

	request_foodbox.box_ip = request.META["REMOTE_ADDR"]
	now = time.localtime()
	now_datetime = datetime.datetime(
		now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec,
		tzinfo=datetime.timezone(offset=datetime.timedelta())
	)
	request_foodbox.box_last_sync = now_datetime
	request_foodbox.save()

	for cardopen in cards_to_sync:
		cardopen.synced = True
		cardopen.save()

	response_json = json.dumps({"admin_cards": admin_cards_list, "modified_cards": [], "new_cards": cards_to_sync_list})
	response = HttpResponse(content=response_json, content_type="application/json", status=200)
	my_log = SystemLog(
		time_stamp=time.time(),
		message="pullcards from FoodBox succeeded.",
		message_type="Information",
		severity=0
	)
	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	BrainBoxDB.add_system_log(myLog=my_log)
	return response


def pullfoodbox(request, box_id):
	try:
		request_current_weight = float(request.GET.get("current_weight"))  # type: float
	except (ValueError, AttributeError) as e:
		my_log = SystemLog(
			time_stamp=time.time(),
			message="Unexpected request body: {0}".format(str(e.args)),
			message_type="Fatal",
			severity=2
		)
		print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
		BrainBoxDB.add_system_log(myLog=my_log)
		return HttpResponse(status=400)

	request_foodbox = BrainBoxDB.get_foodBox_by_foodBox_id(box_id)  # type: FoodBox
	request_box_ip = request.META["REMOTE_ADDR"]
	now = time.localtime()
	now_datetime = datetime.datetime(
		now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec,
		tzinfo=datetime.timezone(offset=datetime.timedelta())
	)

	if not request_foodbox:
		request_foodbox = FoodBox.objects.create(
			box_id=box_id, box_ip=request_box_ip, box_name="FoodBox_{}".format(box_id), box_last_sync=now_datetime,
			current_weight=request_current_weight, synced_to_foodbox=True,
			synced_to_server=False
		)
	else:
		request_foodbox.box_ip = request_box_ip
		request_foodbox.box_last_sync = now_datetime
		request_foodbox.current_weight = request_current_weight
		request_foodbox.synced_to_foodbox=True
		request_foodbox.synced_to_server=False
	request_foodbox.save()

	response_json = json.dumps({"foodbox_name": request_foodbox.box_name})
	response = HttpResponse(content=response_json, content_type="application/json", status=200)
	my_log = SystemLog(
		time_stamp=time.time(),
		message="pullfoodbox from FoodBox succeeded.",
		message_type="Information",
		severity=0
	)
	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	BrainBoxDB.add_system_log(myLog=my_log)
	return response
