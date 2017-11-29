from bbox.bboxDB import BrainBoxDB
from bbox.models import Account
from bbox.models import Card
from bbox.models import FeedingLog
from bbox.models import FoodBox
from bbox.models import SystemLog
from bbox.models import SystemSetting
from datetime import datetime
import json
import pytz
import requests
import time


def put_foodboxes():
	my_account = BrainBoxDB.get_account_info()  # type: Account
	server_address = BrainBoxDB.get_system_setting("Server_Address")  # type: SystemSetting
	server_authentication_user = BrainBoxDB.get_system_setting("Server_Authentication_User")  # type: SystemSetting
	server_authentication_pw = BrainBoxDB.get_system_setting("Server_Authentication_PW")  # type: SystemSetting
	assert my_account is not None
	assert server_address is not None
	assert server_authentication_user is not None
	assert server_authentication_pw is not None

	server_address = server_address.value_text
	my_auth = (server_authentication_user.value_text, server_authentication_pw.value_text)
	server_token_auth = {
		"server-token-user": my_account.user_name,
		"server-token-pw": my_account.server_token
	}
	print("server_token_auth: {0}".format(server_token_auth))  # TODO - Delete debug message
	unsynced_foodboxes = BrainBoxDB.get_unsynced_foodBoxes_to_server()  # type: tuple[FoodBox]
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
			"foodbox_name": foodbox.box_name,
			"current_weight": foodbox.current_weight
		}
		for foodbox in unsynced_foodboxes
	]
	payload = {"foodboxes": foodboxes_to_sync}
	print("Payload FoodBoxes: {0}".format(payload))  # TODO - Delete debug message
	put_address = "https://{0}/api/bbox/put_foodbox".format(server_address)
	print("PUT address FoodBoxes: {0}".format(put_address))  # TODO - Delete debug message

	now = time.time()
	try:
		server_response = requests.put(
			url=put_address, json=payload, auth=my_auth, headers=server_token_auth
		)
		if server_response.status_code != 200 and server_response.status_code != 204:
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

			for tmp_foodbox in unsynced_foodboxes:
				tmp_foodbox.synced_to_server = True
				tmp_foodbox.save()
	except Exception as e:
		my_log = SystemLog(
			time_stamp=now,
			message="Failed to PUT FoodBox on server - Exception: {0}".format(
				str(e.args)
			),
			message_type="Error",
			severity=2
		)

	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	BrainBoxDB.add_system_log(myLog=my_log)

	now = datetime.now().replace(microsecond=0)
	BrainBoxDB.set_system_setting("Server_Last_Sync", str(now))


def put_feedinglogs():
	server_authentication_user = BrainBoxDB.get_system_setting("Server_Authentication_User")  # type: SystemSetting
	server_authentication_pw = BrainBoxDB.get_system_setting("Server_Authentication_PW")  # type: SystemSetting
	my_account = BrainBoxDB.get_account_info()  # type: Account
	server_address = BrainBoxDB.get_system_setting("Server_Address")  # type: SystemSetting
	assert my_account is not None
	assert server_address is not None
	assert server_authentication_user is not None
	assert server_authentication_pw is not None

	server_address = server_address.value_text
	my_auth = (server_authentication_user.value_text, server_authentication_pw.value_text)
	server_token_auth = {
		"server-token-user": my_account.user_name,
		"server-token-pw": my_account.server_token
	}
	print("server_token_auth: {0}".format(server_token_auth))  # TODO - Delete debug message
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
			"foodbox_id": feeding_log.foodbox.box_id,
			"feeding_id": feeding_log.feeding_id,
			"card_id": feeding_log.card.card_id,
			"open_time": feeding_log.open_time.replace(
				tzinfo=pytz.timezone("UTC")
			).astimezone(
				pytz.timezone("Asia/Jerusalem")
			).strftime(
				"%Y-%m-%d %H:%M:%S"
			),
			"close_time": feeding_log.close_time.replace(
				tzinfo=pytz.timezone("UTC")
			).astimezone(
					pytz.timezone("Asia/Jerusalem")
			).strftime(
				"%Y-%m-%d %H:%M:%S"
			),
			"start_weight": feeding_log.start_weight,
			"end_weight": feeding_log.end_weight
		}
		for feeding_log in unsynced_feeding_logs
	]
	payload = {"feeding_logs": feeding_logs_to_sync}
	print("Payload FeedingLogs: {0}".format(payload))  # TODO - Delete debug message
	put_address = "https://{0}/api/bbox/put_feeding_log".format(server_address)
	print("PUT address FeedingLogs: {0}".format(put_address))  # TODO - Delete debug message

	now = time.time()
	try:
		server_response = requests.put(
			url=put_address, json=payload, auth=my_auth, headers=server_token_auth
		)
		if server_response.status_code != 200 and server_response.status_code != 201:
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
				message="PUT FeedingLog on server succeeded: {0}".format(
					payload
				),
				message_type="Information",
				severity=0
			)

			for feeding_log in unsynced_feeding_logs:
				feeding_log.synced = True
				feeding_log.save()

	except Exception as e:
		my_log = SystemLog(
			time_stamp=now,
			message="Failed to PUT FeedingLog on server - Exception: {0}".format(
				str(e.args)
			),
			message_type="Error",
			severity=2
		)

	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	BrainBoxDB.add_system_log(myLog=my_log)

	now = datetime.now().replace(microsecond=0)
	BrainBoxDB.set_system_setting("Server_Last_Sync", str(now))


def get_server_token(user_name: str, password: str):
	server_authentication_user = BrainBoxDB.get_system_setting("Server_Authentication_User")  # type: SystemSetting
	server_authentication_pw = BrainBoxDB.get_system_setting("Server_Authentication_PW")  # type: SystemSetting
	brainbox_id = BrainBoxDB.get_system_setting("BrainBox_ID")  # type: SystemSetting
	server_address = BrainBoxDB.get_system_setting("Server_Address")  # type: SystemSetting
	assert brainbox_id is not None
	assert server_address is not None
	assert server_authentication_user is not None
	assert server_authentication_pw is not None

	server_address = server_address.value_text
	my_auth = (server_authentication_user.value_text, server_authentication_pw.value_text)
	server_token_auth = {
		"server-token-user": user_name,
		"server-token-pw": password
	}
	print("server_token_auth: {0}".format(server_token_auth))  # TODO - Delete debug message

	payload = {"brainbox_id": brainbox_id.value_text}
	print("Payload server_token: {0}".format(payload))  # TODO - Delete debug message
	get_address = "https://{0}/api/bbox/get_server_token".format(server_address)
	print("GET address server_token: {0}".format(get_address))  # TODO - Delete debug message

	now = time.time()
	new_server_token = None
	login_status = False
	try:
		server_response = requests.get(
			url=get_address, json=payload, auth=my_auth, headers=server_token_auth
		)
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
			login_status = True

	except (ValueError, AttributeError) as e:
		my_log = SystemLog(
			time_stamp=now,
			message="Server returned unexpected response: {0}".format(
				str(e.args)
			),
			message_type="Fatal",
			severity=2
		)
	except Exception as e:
		my_log = SystemLog(
			time_stamp=now,
			message="Failed to GET server_token from server - Exception: {0}".format(
				str(e.args)
			),
			message_type="Error",
			severity=2
		)

	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	BrainBoxDB.add_system_log(myLog=my_log)

	now = datetime.now().replace(microsecond=0)
	BrainBoxDB.set_system_setting("Server_Last_Sync", str(now))

	return new_server_token, login_status


def head_check_server_connection():
	server_authentication_user = BrainBoxDB.get_system_setting("Server_Authentication_User")  # type: SystemSetting
	server_authentication_pw = BrainBoxDB.get_system_setting("Server_Authentication_PW")  # type: SystemSetting
	server_address = BrainBoxDB.get_system_setting("Server_Address")  # type: SystemSetting
	assert server_address is not None
	assert server_authentication_user is not None
	assert server_authentication_pw is not None

	server_address = server_address.value_text
	head_address = "https://{0}/api/bbox/head_check_server_connection".format(
		server_address
	)
	print("HEAD address check_server_connection: {0}".format(head_address))  # TODO - Delete debug message
	my_auth = (server_authentication_user.value_text, server_authentication_pw.value_text)

	now = time.time()
	try:
		server_response = requests.head(url=head_address, auth=my_auth, allow_redirects=True)

		if server_response.status_code != 200 and server_response.status_code != 204:
			my_log = SystemLog(
				time_stamp=now,
				message="Failed to HEAD check_server_connection from server - status_code {0}".format(
					server_response.status_code
				),
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
			message="Failed to HEAD check_server_connection from server - Exception: {0}".format(
				str(e.args)
			),
			message_type="Error",
			severity=2
		)
		server_status = False

	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	BrainBoxDB.add_system_log(myLog=my_log)
	return server_status

