from bbox.bboxDB import BrainBoxDB
from bbox.models import Account
from bbox.models import Card
from bbox.models import CardOpen
from bbox.models import FoodBox
from bbox.models import SystemLog
from bbox.models import SystemSetting
from datetime import datetime
import json
import requests
import time


def get_cards():
	my_account = BrainBoxDB.get_account_info()  # type: Account
	server_address = BrainBoxDB.get_system_setting("Server_Address")  # type: SystemSetting
	server_authentication_user = BrainBoxDB.get_system_setting("Server_Authentication_User")  # type: SystemSetting
	server_authentication_pw = BrainBoxDB.get_system_setting("Server_Authentication_PW")  # type: SystemSetting
	assert my_account is not None
	assert server_address is not None
	assert server_authentication_user is not None
	assert server_authentication_pw is not None

	my_auth = (server_authentication_user.value_text, server_authentication_pw.value_text)

	server_token_auth = {
		"server-token-user": my_account.user_name,
		"server-token-pw": my_account.server_token
	}
	print("server_token_auth: {0}".format(server_token_auth))  # TODO - Delete debug message
	server_address = server_address.value_text
	get_address = "https://{0}/api/bbox/get_card".format(server_address)
	print("GET address get_card: {0}".format(get_address))  # TODO - Delete debug message

	now = time.time()
	try:
		server_response = requests.get(
			url=get_address, auth=my_auth, headers=server_token_auth
		)
		cards_response = json.loads(server_response.text)

		admin_cards_response = cards_response["admin_cards"]
		regular_cards_response = cards_response["regular_cards"]

		all_foodboxes = FoodBox.objects.all()

		for card in admin_cards_response:
			card_obj, card_created = Card.objects.update_or_create(
				card_id=card["card_id"],
				defaults={
					"card_id": card["card_id"],
					"card_name": card["card_name"],
					"admin": True
				},
			)
			for foodbox in all_foodboxes:
				card_open_obj, card_open_created = CardOpen.objects.update_or_create(
					card=card_obj, foodbox=foodbox,
					defaults={
						"active": card["active"],
						"changed_date": card["update_time"],
						"synced": False
					},
				)

		for card in regular_cards_response:
			try:
				tmp_foodbox = FoodBox.objects.get(box_id=card["foodbox_id"])  # type: FoodBox
				card_obj, card_created = Card.objects.update_or_create(
					card_id=card["card_id"],
					defaults={
						"card_id": card["card_id"],
						"card_name": card["card_name"],
						"admin": False
					},
				)
				card_open_obj, card_open_created = CardOpen.objects.update_or_create(
					card=card_obj, foodbox=tmp_foodbox,
					defaults={
						"active": card["active"],
						"changed_date": card["update_time"],
						"synced": False
					},
				)
			except FoodBox.DoesNotExist:
				my_log = SystemLog(
					time_stamp=now,
					message="Server returned unexpected FoodBox: {0}".format(
						card["foodbox_id"]
					),
					message_type="Fatal",
					severity=1
				)
				print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
				BrainBoxDB.add_system_log(myLog=my_log)

		my_log = SystemLog(
			time_stamp=now,
			message="GET card from server succeeded.",
			message_type="Information",
			severity=0
		)

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
			message="Failed to GET cards from server - Exception: {0}".format(
				str(e.args)
			),
			message_type="Error",
			severity=2
		)

	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	BrainBoxDB.add_system_log(myLog=my_log)

	now = datetime.now().replace(microsecond=0)
	BrainBoxDB.set_system_setting("Server_Last_Sync", str(now))


def get_foodboxes():
	# TODO - SSL
	my_account = BrainBoxDB.get_account_info()  # type: Account
	server_address = BrainBoxDB.get_system_setting("Server_Address")  # type: SystemSetting
	server_authentication_user = BrainBoxDB.get_system_setting("Server_Authentication_User")  # type: SystemSetting
	server_authentication_pw = BrainBoxDB.get_system_setting("Server_Authentication_PW")  # type: SystemSetting
	assert my_account is not None
	assert server_address is not None
	assert server_authentication_user is not None
	assert server_authentication_pw is not None

	my_auth = (server_authentication_user.value_text, server_authentication_pw.value_text)
	server_token_auth = {
		"server-token-user": my_account.user_name,
		"server-token-pw": my_account.server_token
	}
	print("server_token_auth: {0}".format(server_token_auth))  # TODO - Delete debug message

	server_address = server_address.value_text
	get_address = "https://{0}/api/bbox/get_foodbox".format(server_address)
	print("GET address get_foodbox: {0}".format(get_address))  # TODO - Delete debug message

	now = time.time()
	try:
		server_response = requests.get(
			url=get_address, auth=my_auth, headers=server_token_auth
		)
		foodboxes_response = json.loads(server_response.text)

		for foodbox in foodboxes_response['foodboxes']:
			try:
				tmp_foodbox = FoodBox.objects.get(
					box_id=foodbox["foodbox_id"]
				)  # type: FoodBox
				tmp_foodbox.box_name = foodbox["foodbox_name"]
				tmp_foodbox.synced_to_foodbox = False
				tmp_foodbox.save()
			except FoodBox.DoesNotExist:
				my_log = SystemLog(
					time_stamp=now,
					message="Server returned unexpected FoodBox: {0}".format(
						foodbox["foodbox_id"]
					),
					message_type="Fatal",
					severity=1
				)
				print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
				BrainBoxDB.add_system_log(myLog=my_log)

		my_log = SystemLog(
			time_stamp=now,
			message="GET foodboxes from server succeeded.",
			message_type="Information",
			severity=0
		)
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
			message="Failed to GET foodboxes from server - Exception: {0}".format(
				str(e.args)
			),
			message_type="Error",
			severity=2
		)

	print("Writing SystemLog: {0}".format(my_log))  # TODO - Delete debug message
	BrainBoxDB.add_system_log(myLog=my_log)

