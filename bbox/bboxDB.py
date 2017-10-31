from .models import Account
from .models import Card
from .models import CardOpen
from .models import FeedingLog
from .models import FoodBox
from .models import SystemLog
from .models import SystemSetting
from datetime import datetime
from itertools import chain
import pytz
import time


class BrainBoxDB:
	### Start feeding_logs functiones ###

	@staticmethod
	def get_feeding_log_by_id(logID: str):
		"""
		Function gets a feeding_log ID (The original UUID) and returns a feeding_log OBJECT
		"""
		return FeedingLog.objects.filter(feeding_id=logID).first()

	@staticmethod
	def get_all_feeding_logs():
		"""
		Returns a tuple of all feeding logs
		"""
		return tuple(FeedingLog.objects.all())

	@staticmethod
	def get_synced_feeding_logs():
		"""
		Returns a tuple of synced feeding logs
		"""
		return tuple(FeedingLog.objects.filter(synced=1))

	@staticmethod
	def get_not_synced_feeding_logs():
		"""
		Returns a tuple of synced feeding logs
		"""
		return tuple(FeedingLog.objects.filter(synced=0))

	@staticmethod
	def set_feeding_log_synced(myLogUID: str):
		"""
		Get feeding_log UID and change the synced status to True = 1
		"""
		FeedingLog.objects.filter(feeding_id=myLogUID).update(synced=1)

	@staticmethod
	def set_feeding_log_not_synced(myLogUID: str):
		"""
		Get feeding_log UID and change the synced status to False = 0
		"""
		FeedingLog.objects.filter(feeding_id=myLogUID).update(synced=0)

	@staticmethod
	def delete_synced_feeding_logs():
		"""
		Delete all synced feeding_logs from the DB
		"""
		FeedingLog.objects.filter(synced=1).delete()

	@staticmethod
	def get_feeding_logs_by_box_id(boxId):
		return tuple(FeedingLog.objects.filter(foodbox=boxId))

	@staticmethod
	def add_feeding_log(myLog: FeedingLog):
		"""
		Getting a feeding_log as an object and Adding it to the DB
		"""
		FeedingLog.objects.create(
			foodbox=myLog.foodbox,
			feeding_id=myLog.feeding_id,
			card=myLog.card,
			open_time=myLog.open_time,
			close_time=myLog.close_time,
			start_weight=myLog.start_weight,
			end_weight=myLog.end_weight,
			synced=myLog.synced
		)

	### END of feeding_logs functiones ###

	### Start of system_logs functions ###

	@staticmethod
	def get_system_log_by_id(logID: int):
		"""
		Function gets a SystemLog ID and returns a SystemLog object or None if no such object
		"""
		return SystemLog.objects.filter(rowid=logID).first()

	@staticmethod
	def get_all_system_logs():
		"""Returns a tuple of all system logs since logs_since, or all of them
		"""
		return tuple(SystemLog.objects.all())

	@staticmethod
	def add_system_log(myLog: SystemLog):
		"""
		Function gets a SystemLog object and writes it to the database
		"""
		SystemLog.objects.create(
			time_stamp=datetime.fromtimestamp(
				myLog.time_stamp,
				pytz.timezone("Asia/Jerusalem")
			),
			message=myLog.message,
			message_type=myLog.message_type,
			severity=myLog.severity
		)

	### End of system_logs functions ###

	### Start of system_settings functiones ###

	@staticmethod
	def get_system_setting(setting: str):
		"""Function returns a value of a specific setting from enums that are available:
			the input must be "SystemSettings.key_name"
			key names: BrainBox_ID / BrainBox_Name / Sync_Interval / Server_Address
			If the key_name is still not written in the DB or has no value it returns None
		"""
		return SystemSetting.objects.filter(key_name=setting).first()

	@staticmethod
	def set_system_setting(setting: str, value: str):
		"""
		Function sets a value to a key in "system_settings" table
		If the key doesn't exist yet , it will write a new row with the key and value
		"""
		SystemSetting.objects.update_or_create(defaults={"value_text": value}, key_name=setting)

	### END of system_logs functions ###

	### Start of Account functions ###

	@staticmethod
	def get_account_info():
		"""
		Returns account info: username&password
		"""
		return Account.objects.all().first()

	@staticmethod
	def add_account(user: str, password: str):
		"""
		add a new account to DB
		"""
		Account.objects.create(user_name=user, password=password)

	@staticmethod
	def change_user_name_and_or_password(acc: Account, new_user_name: str = None, new_password: str = None):
		"""
		Function receives an account and changes user_name and/or password
		"""
		currentAccount = acc
		if new_password is not None:
			Account.objects.filter(user_name=currentAccount.user_name).update(password=new_password)
		if new_user_name is not None:
			Account.objects.filter(user_name=currentAccount.user_name).update(user_name=new_user_name)

	### END of Account functions ###

	### Start of FoodBox functions ###

	@staticmethod
	def get_all_foodBoxes():
		"""
		Returns a tuple of all food_boxes
		"""
		return tuple(FoodBox.objects.all())

	@staticmethod
	def get_unsynced_foodBoxes_to_foodbox():
		"""
		Returns a tuple of unsynced_to_foodbox food_boxes
		"""
		queryset = FoodBox.objects.filter(synced_to_foodbox=False)
		return tuple([entry for entry in queryset])

	@staticmethod
	def get_unsynced_foodBoxes_to_server():
		"""
		Returns a tuple of unsynced_to_server food_boxes
		"""
		queryset = FoodBox.objects.filter(synced_to_server=False)
		return tuple([entry for entry in queryset])

	@staticmethod
	def delete_foodBox(foodBox: FoodBox):
		"""
		Delete a foodbox from the table
		"""
		FoodBox.objects.filter(box_id=foodBox.box_id).delete()

	@staticmethod
	def get_foodBox_by_foodBox_id(boxId: str):
		"""
		Returns a specific foodbox by ID
		"""
		return FoodBox.objects.filter(box_id=boxId).first()

	### END of FoodBox functions ###
	### Start of Cards functions ###

	@staticmethod
	def get_all_cards():
		return tuple(Card.objects.all())

	@staticmethod
	def get_cards(admin=False):
		# if admin=false return all NON admin cards
		# if admin=true return all admin cards
		return tuple(Card.objects.filter(admin=admin))

	@staticmethod
	def get_boxes_for_card(card_id: str):
		#returns tupple of foodBoxes
		queryset = CardOpen.objects.filter(card=card_id)
		boxes_ids = [entry.foodbox.box_id for entry in queryset]
		return tuple(boxes_ids)

	@staticmethod
	def get_cards_for_box(box_id: str, active_only: bool = True):
		#returns tupple of cards
		if active_only:
			queryset = CardOpen.objects.filter(foodbox=box_id, active=True)
		else:
			queryset = CardOpen.objects.filter(foodbox=box_id)
		cards = [entry.card for entry in queryset]
		return tuple(cards)

	@staticmethod
	def get_unsynced_cards_for_box(box_id: str):
		queryset = CardOpen.objects.filter(foodbox=box_id, synced=False)
		return tuple([entry for entry in queryset])

	@staticmethod
	def set_card_name(card_id: str, new_name: str):
		Card.objects.filter(card_id=card_id).update(card_name=new_name)

	@staticmethod
	def get_card_by_name(card_name: str):
		return Card.objects.filter(card_name=card_name)

	@staticmethod
	def add_card(card_id: str, card_name: str = None, isAdmin: bool = False):
		Card.objects.create(card_id=card_id, card_name=card_name, admin=isAdmin)

	@staticmethod
	def set_card_active_for_box(card_id: str, box_id: str):
		CardOpen.objects.filter(card=card_id, foodbox=box_id).update(active=True)

	@staticmethod
	def set_card_not_active_for_box(card_id: str, box_id: str):
		CardOpen.objects.filter(card=card_id, foodbox=box_id).update(active=False)

	@staticmethod
	def associate_card_with_box(card_id: str, box_id: str):
		#add active card with box to CardOpen table
		CardOpen.objects.create(
			card=card_id,
			foodbox=box_id,
			active=True,
			changed_date=datetime.now()
		)

	@staticmethod
	def delete_card(card_id: str):
		Card.objects.filter(card_id=card_id).delete()
	### END of Cards functions ###

