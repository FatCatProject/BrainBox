import os.path
import sqlite3
import time
import datetime
from .models import FeedingLog, Account, FoodBox, SystemLog, SystemSetting


class BrainBoxDB:
	def __init__(self):
		# Check if DB exists , if not - create it
		self.conn = sqlite3.connect('db.sqlite3')
		self.c = self.conn.cursor()  # type: sqlite3.Cursor
		self.c.execute("PRAGMA foreign_keys = ON")

	def __del__(self):
		self.c.close()
		self.conn.close()

	### Start feeding_logs functiones ###
	def get_feeding_log_by_id(self, logID: str):
		"""
		Function gets a feeding_log ID (The original UUID) and returns a feeding_log OBJECT
		"""
		return FeedingLog.objects.filter(feeding_id=logID)

	def get_all_feeding_logs(self):
		"""
		Returns a tuple of all feeding logs
		"""
		return FeedingLog.objects.all()

	def get_synced_feeding_logs(self):
		"""
		Returns a tuple of synced feeding logs
		"""
		return FeedingLog.objects.filter(synced=1)

	def get_not_synced_feeding_logs(self):
		"""
		Returns a tuple of synced feeding logs
		"""
		return FeedingLog.objects.filter(synced=0)

	def set_feeding_log_synced(self, myLogUID: str):
		"""
		Get feeding_log UID and change the synced status to True = 1
		"""
		FeedingLog.objects.filter(feeding_id=myLogUID).update(synced=1)

	def set_feeding_log_not_synced(self, myLogUID: str):
		"""
		Get feeding_log UID and change the synced status to False = 0
		"""
		FeedingLog.objects.filter(feeding_id=myLogUID).update(synced=0)

	def delete_synced_feeding_logs(self):
		"""
		Delete all synced feeding_logs from the DB
		"""
		FeedingLog.objects.filter(synced=1).delete()

	def get_feeding_logs_by_box_id(self, boxId):
		return FeedingLog.objects.filter(box_id=boxId)

	def add_feeding_log(self, myLog: FeedingLog):
		"""
		Getting a feeding_log as an object and Adding it to the DB
		"""
		FeedingLog.objects.create(box_id=myLog.box_id,
								  feeding_id=myLog.feeding_id,
								  card_id=myLog.card_id,
								  open_time=myLog.open_time,
								  close_time=myLog.close_time,
								  start_weight=myLog.start_weight,
								  end_weight=myLog.end_weight,
								  synced=myLog.synced)

	### END of feeding_logs functiones ###

	### Start of system_logs functions ###
	def get_system_log_by_id(self, logID: int):
		"""
		Function gets a SystemLog ID and returns a SystemLog object or None if no such object
		"""
		return SystemLog.objects.filter(rowid=logID)

	def get_all_system_logs(self):
		"""Returns a tuple of all system logs since logs_since, or all of them
		"""
		return SystemLog.objects.filter()

	def add_system_log(self, myLog: SystemLog):
		"""
		Function gets a SystemLog object and writes it to the database
		"""
		SystemLog.objects.create(time_stamp=myLog.time_stamp,
								 message=myLog.message,
								 message_type=myLog.message_type,
								 severity=myLog.severity)

	### End of system_logs functions ###

	### Start of system_settings functiones ###
	def get_system_setting(self, setting: str):
		"""Function returns a value of a specific setting from enums that are available:
			the input must be "SystemSettings.key_name"
			key names: BrainBox_ID / BrainBox_Name / Sync_Interval
			If the key_name is still not written in the DB or has no value it returns None
		"""
		return SystemSetting.objects.filter(key_name=setting)

	def set_system_setting(self, setting: str, value: str):
		"""
		Function sets a value to a key in "system_settings" table
		If the key doesn't exist yet , it will write a new row with the key and value
		"""
		SystemSetting.objects.filter(key_name=setting).update(value_text=value)

	### END of system_logs functions ###

	### Start of Account functions ###
	def get_account_info(self):
		"""
		Returns ALL account info: username&password
		"""
		return Account.objects.all()

	def add_account(self, account: Account):
		"""
		add a new account to DB
		"""
		Account.objects.create(user_name=account.user_name,
							   password=account.password)

	def change_user_name_and_or_password(self, acc: Account, new_user_name: str = None, new_password: str = None):
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
	def get_all_foodBoxes(self):
		"""
		Returns a tuple of all food_boxes
		"""
		return FoodBox.objects.all()

	def delete_foodBox(self, foodBox: FoodBox):
		"""
		Delete a foodbox from the table
		"""
		FoodBox.objects.filter(box_id=foodBox.box_id).delete()

	def get_foodBox_by_foodBox_id(self, boxId: str):
		"""
		Returns a specific foodbox by ID
		"""
		return FoodBox.objects.filter(box_id=boxId)
		### END of FoodBox functions ###
