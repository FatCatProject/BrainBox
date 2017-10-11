import json
import requests
import time
import datetime
from bbox.models import Account, Card, FeedingLog, FoodBox, SystemLog, SystemSetting
from bbox.bboxDB import BrainBoxDB


def put_foodboxes():
	# TODO - SSL
	my_account = BrainBoxDB.get_account_info()  # type: Account
	server_address = BrainBoxDB.get_system_setting("Server_Address")  # type: SystemSetting
	assert my_account is not None
	assert server_address is not None

	server_address = server_address.value_text
	my_auth = (my_account.user_name, my_account.server_token)
	print("my_auth: {0}".format(my_auth))  # TODO - Delete debug message
	unsynced_foodboxes = BrainBoxDB.get_unsynced_foodBoxes()  # type: tuple[FoodBox]
	if not unsynced_foodboxes:
		now = time.time()
		my_log = SystemLog(
			time_stamp=now,
			message="No FoodBoxes to PUT on server",
			message_type="Information",
			severity=0
		)
		print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
		BrainBoxDB.add_system_log(myLog=my_log)
		return

	foodboxes_to_sync = [
		{
			"foodbox_id": foodbox.box_id,
			"foodbox_name": foodbox.box_name
		}
		for foodbox in unsynced_foodboxes
	]
	payload = {"foodboxes": foodboxes_to_sync}
	print("Payload FoodBoxes: {0}".format(payload))  # TODO - Delete debug message
	put_address = "http://{0}/bbox/put_foodbox/".format(server_address)
	print("PUT address FoodBoxes: {0}".format(put_address))  # TODO - Delete debug message

	now = time.time()
	try:
		server_response = requests.put(url=put_address, json=payload, auth=my_auth)
		if server_response.status_code != 200:
			my_log = SystemLog(
				time_stamp=now,
				message="Failed to PUT FoodBox on server: {0} - status_code: {1}".format(
					payload,
					server_response.status_code
				),
				message_type="Error",
				severity=2
			)
		else:
			my_log = SystemLog(
				time_stamp=now,
				message="PUT FoodBox on server succeeded: {0}".format(payload),
				message_type="Information",
				severity=0
			)

			for foodbox in unsynced_foodboxes:
				foodbox.synced = True
				foodbox.save()
	except Exception as e:
		my_log = SystemLog(
			time_stamp=now,
			message="Failed to PUT FoodBox on server - Exception: {0}".format(e.args),
			message_type="Error",
			severity=2
		)

	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	BrainBoxDB.add_system_log(myLog=my_log)

	# server_address = "http://{0}/bbox/put_foodbox/".format(server_address)
	# for foodbox in unsynced_foodboxes:
	# 	payload = {
	# 		"foodbox_id": foodbox.box_id,
	# 		"foodbox_name": foodbox.box_name
	# 	}
	# 	print("Sending FoodBox: {0}".format(payload))  # TODO - Delete debug message
	# 	put_address = server_address + "{0}".format(foodbox.box_id)
	# 	server_response = requests.put(url=put_address, json=payload, auth=my_auth)
	#
	# 	now = time.time()
	# 	if server_response.status_code != 200:
	# 		my_log = SystemLog(
	# 			time_stamp=now,
	# 			message="Failed to PUT FoodBox on server: {0}".format(payload),
	# 			message_type="Error",
	# 			severity=2
	# 		)
	# 	else:
	# 		my_log = SystemLog(
	# 			time_stamp=now,
	# 			message="PUT FoodBox on server succeeded: {0}".format(payload),
	# 			message_type="Information",
	# 			severity=0
	# 		)
	# 		foodbox.synced = True
	# 		foodbox.save()
	# 	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	# 	BrainBoxDB.add_system_log(myLog=my_log)
	# 	time.sleep(1)  # No need to rush anything at the moment.

	now = time.time()
	BrainBoxDB.set_system_setting("Server_Last_Sync", str(now))


def put_foodlogs():
	# TODO - SSL
	my_account = BrainBoxDB.get_account_info()  # type: Account
	server_address = BrainBoxDB.get_system_setting("Server_Address")  # type: SystemSetting
	assert my_account is not None
	assert server_address is not None

	server_address = server_address.value_text
	my_auth = (my_account.user_name, my_account.server_token)
	print("my_auth: {0}".format(my_auth))  # TODO - Delete debug message
	unsynced_feeding_logs = BrainBoxDB.get_not_synced_feeding_logs()  # type: tuple[FeedingLog]
	if not unsynced_feeding_logs:
		now = time.time()
		my_log = SystemLog(
			time_stamp=now,
			message="No FeedingLogs to PUT on server",
			message_type="Information",
			severity=0
		)
		print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
		BrainBoxDB.add_system_log(myLog=my_log)
		return

	feeding_logs_to_sync = [
		{
			"foodbox_id": feeding_log.box_id.box_id,
			"feeding_id": feeding_log.feeding_id,
			"card_id": feeding_log.card_id.card_id,
			"open_time": str(feeding_log.open_time),
			"close_time": str(feeding_log.close_time),
			"start_weight": feeding_log.start_weight,
			"end_weight": feeding_log.end_weight
		}
		for feeding_log in unsynced_feeding_logs
	]
	payload = {"feeding_logs": feeding_logs_to_sync}
	print("Payload FeedingLogs: {0}".format(payload))  # TODO - Delete debug message
	put_address = "http://{0}/bbox/put_feeding_log/".format(server_address)
	print("PUT address FeedingLogs: {0}".format(put_address))  # TODO - Delete debug message

	now = time.time()
	try:
		server_response = requests.put(url=put_address, json=payload, auth=my_auth)
		if server_response.status_code != 200:
			my_log = SystemLog(
				time_stamp=now,
				message="Failed to PUT FeedingLog on server: {0} - status_code: {1}".format(
					payload,
					server_response.status_code
				),
				message_type="Error",
				severity=2
			)
		else:
			my_log = SystemLog(
				time_stamp=now,
				message="PUT FeedingLog on server succeeded: {0}".format(payload),
				message_type="Information",
				severity=0
			)

			for feeding_log in unsynced_feeding_logs:
				feeding_log.synced = True
				feeding_log.save()

	except Exception as e:
		my_log = SystemLog(
			time_stamp=now,
			message="Failed to PUT FeedingLog on server - Exception: {0}".format(e.args),
			message_type="Error",
			severity=2
		)

	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	BrainBoxDB.add_system_log(myLog=my_log)

	# server_address = "http://{0}/bbox/put_feeding_log/".format(server_address)
	# for feeding_log in unsynced_feeding_logs:
	# 	payload = {
	# 		"foodbox_id": feeding_log.box_id,
	# 		"feeding_id": feeding_log.feeding_id,
	# 		"card_id": feeding_log.card_id.card_id,
	# 		"open_time": str(feeding_log.open_time),
	# 		"close_time": str(feeding_log.close_time),
	# 		"start_weight": feeding_log.start_weight,
	# 		"end_weight": feeding_log.end_weight
	# 	}
	#
	# 	print("Sending FeedingLog: {0}".format(payload))  # TODO - Delete debug message
	# 	put_address = server_address + "{0}".format(feeding_log.feeding_id)
	# 	server_response = requests.put(url=put_address, json=payload, auth=my_auth)
	#
	# 	now = time.time()
	# 	if server_response.status_code != 200:
	# 		my_log = SystemLog(
	# 			time_stamp=now,
	# 			message="Failed to PUT FeedingLog on server: {0}".format(payload),
	# 			message_type="Error",
	# 			severity=2
	# 		)
	# 	else:
	# 		my_log = SystemLog(
	# 			time_stamp=now,
	# 			message="PUT FeedingLog on server succeeded: {0}".format(payload),
	# 			message_type="Information",
	# 			severity=0
	# 		)
	# 		feeding_log.synced = True
	# 		feeding_log.save()
	# 	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	# 	BrainBoxDB.add_system_log(myLog=my_log)
	# 	time.sleep(1)  # No need to rush anything at the moment.

	now = time.time()
	BrainBoxDB.set_system_setting("Server_Last_Sync", str(now))


def get_server_token(user_name: str, password: str):
	# TODO - SSL
	server_address = BrainBoxDB.get_system_setting("Server_Address")  # type: SystemSetting
	assert server_address is not None

	server_address = server_address.value_text
	my_auth = (user_name, password)
	print("my_auth: {0}".format(my_auth))  # TODO - Delete debug message

	put_address = "http://{0}/bbox/get_server_token/".format(server_address)
	print("PUT address server_token: {0}".format(put_address))  # TODO - Delete debug message

	now = time.time()
	new_server_token = None
	login_status = False
	try:
		server_response = requests.put(url=put_address, auth=my_auth)
		if server_response.status_code != 200:
			my_log = SystemLog(
				time_stamp=now,
				message="Failed to GET server_token from server - status_code {0}".format(
					server_response.status_code
				),
				message_type="Error",
				severity=2
			)
		else:
			my_log = SystemLog(
				time_stamp=now,
				message="GET server_token from server succeeded.",
				message_type="Information",
				severity=0
			)

			server_response = json.loads(server_response.text)

			new_server_token = server_response['server_token']
			login_status = server_response['login_status']

	except (json.decoder.JSONDecodeError, AttributeError) as e:
		my_log = SystemLog(
			time_stamp=now,
			message="Server returned unexpected response: {0}".format(e.args),
			message_type="Fatal",
			severity=2
		)
	except Exception as e:
		my_log = SystemLog(
			time_stamp=now,
			message="Failed to GET server_token from server - Exception: {0}".format(e.args),
			message_type="Error",
			severity=2
		)

	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	BrainBoxDB.add_system_log(myLog=my_log)

	now = time.time()
	BrainBoxDB.set_system_setting("Server_Last_Sync", str(now))

	return new_server_token, login_status


def head_check_server_connection():
	server_address = BrainBoxDB.get_system_setting("Server_Address")  # type: SystemSetting
	assert server_address is not None

	server_address = server_address.value_text
	put_address = "http://{0}/bbox/head_check_server_connection/".format(server_address)
	print("HEAD address check_server_connection: {0}".format(put_address))  # TODO - Delete debug message

	now = time.time()
	try:
		server_response = requests.head(url=put_address)

		if server_response.status_code != 200:
			my_log = SystemLog(
				time_stamp=now,
				message="Failed to HEAD check_server_connection from server - status_code {0}".format(
					server_response.status_code),
				message_type="Error",
				severity=2
			)
			server_status = False
		else:
			my_log = SystemLog(
				time_stamp=now,
				message="HEAD check_server_connection from server succeeded.",
				message_type="Information",
				severity=0
			)
			server_status = True
	except Exception as e:
		my_log = SystemLog(
			time_stamp=now,
			message="Failed to HEAD check_server_connection from server - Exception: {0}".format(e.args),
			message_type="Error",
			severity=2
		)
		server_status = False

	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	BrainBoxDB.add_system_log(myLog=my_log)
	return server_status

# from django.core import serializers
# data = serializers.serialize("xml", SomeModel.objects.all())
# XMLSerializer = serializers.get_serializer("xml")
# xml_serializer = XMLSerializer()
# xml_serializer.serialize(queryset)
# data = xml_serializer.getvalue()
