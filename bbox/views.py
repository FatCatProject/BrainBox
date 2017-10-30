from .models import Account
from .models import Card
from .models import FeedingLog
from .models import FoodBox
from .models import SystemLog
from .models import SystemSetting
from bbox.bboxDB import BrainBoxDB
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
import requests
import server_tasks.receive as receive_tasks
import server_tasks.send as send_tasks
import time


@csrf_exempt
def pushlogs(request):
	""" Add FeedingLogs to a specific FoodBox's log and confirm them in the response."""

	try:
		request_body = json.loads(request.body.decode("utf-8"))
		request_foodbox = BrainBoxDB.get_foodBox_by_foodBox_id(
			request_body["box_id"]
		)  # type: FoodBox
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
		card.card_id: card for card in BrainBoxDB.get_cards_for_box(
			box_id=request_foodbox.box_id, active_only=False
		)
	}
	print("asdddd {}".format(request_foodbox.box_id))
	confirmed_ids = []
	for log in request_feedinglogs:
		tmp_feeding_id = log["feeding_id"]
		tmp_card_id = box_cards[log["card_id"]]
		tmp_open_time = log["open_time"]
		tmp_close_time = log["close_time"]
		tmp_start_weight = log["start_weight"]
		tmp_end_weight = log["end_weight"]
		tmp_feedinglog = FeedingLog(
			foodbox=request_foodbox, feeding_id=tmp_feeding_id,
			card=tmp_card_id, open_time=tmp_open_time,
			close_time=tmp_close_time, start_weight=tmp_start_weight,
			end_weight=tmp_end_weight, synced=False
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
	response = HttpResponse(
		content=response_json, content_type="application/json", status=200
	)

	my_log = SystemLog(
		time_stamp=time.time(),
		message="push_logs from FoodBox succeeded.",
		message_type="Information",
		severity=0
	)
	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	BrainBoxDB.add_system_log(myLog=my_log)

	try:
		send_tasks.put_foodboxes()
		send_tasks.put_feedinglogs()
		receive_tasks.get_cards()
		receive_tasks.get_foodboxes()
	except requests.exceptions.RequestException as e:
		my_log = SystemLog(
			time_stamp=time.time(),
			message="Failed to sync with server: {0}".format(e.args),
			message_type="Error",
			severity=1
		)
		print("Writing SystemLog: {0}".format(my_log))  # Debug message
		BrainBoxDB.add_system_log(myLog=my_log)

	return response


def pullcards(request, box_id):
	request_foodbox = BrainBoxDB.get_foodBox_by_foodBox_id(box_id)  # type: FoodBox
	cards_to_sync = BrainBoxDB.get_unsynced_cards_for_box(
		box_id=request_foodbox.box_id
	)
	# admin_cards = BrainBoxDB.get_cards(admin=True)

	cards_to_sync_list = [
		{
			"card_id": cardopen.card.card_id,
			"active": cardopen.active,
			"card_name": cardopen.card.card_name
		}
		for cardopen in cards_to_sync if not cardopen.card.admin
	]
	admin_cards_list = [
		{
			"card_id": cardopen.card.card_id,
			"active": cardopen.active,
			"card_name": "ADMIN"
		}
		for cardopen in cards_to_sync if cardopen.card.admin
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

	response_json = json.dumps(
		{
			"admin_cards": admin_cards_list, "modified_cards": [],
			"new_cards": cards_to_sync_list
		}
	)
	response = HttpResponse(
		content=response_json, content_type="application/json", status=200
	)
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
			box_id=box_id, box_ip=request_box_ip,
			box_name="FoodBox_{}".format(box_id), box_last_sync=now_datetime,
			current_weight=request_current_weight
		)
	else:
		request_foodbox.box_ip = request_box_ip
		request_foodbox.box_last_sync = now_datetime
		request_foodbox.current_weight = request_current_weight
		request_foodbox.synced_to_foodbox=True
		request_foodbox.synced_to_server=False
	request_foodbox.save()

	response_json = json.dumps({"foodbox_name": request_foodbox.box_name})
	response = HttpResponse(
		content=response_json, content_type="application/json", status=200
	)
	my_log = SystemLog(
		time_stamp=time.time(),
		message="pullfoodbox from FoodBox succeeded.",
		message_type="Information",
		severity=0
	)
	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	BrainBoxDB.add_system_log(myLog=my_log)

	try:
		send_tasks.put_foodboxes()
		send_tasks.put_feedinglogs()
		receive_tasks.get_cards()
		receive_tasks.get_foodboxes()
	except requests.exceptions.RequestException as e:
		my_log = SystemLog(
			time_stamp=time.time(),
			message="Failed to sync with server: {0}".format(e.args),
			message_type="Error",
			severity=1
		)
		print("Writing SystemLog: {0}".format(my_log))  # Debug message
		BrainBoxDB.add_system_log(myLog=my_log)

	return response

