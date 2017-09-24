from .models import FeedingLog, Account, FoodBox, SystemLog, SystemSetting
import time
import datetime

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
		return tuple(FeedingLog.objects.filter(box_id=boxId))

	@staticmethod
	def add_feeding_log(myLog: FeedingLog):
		"""
		Getting a feeding_log as an object and Adding it to the DB
		"""
		open_t = time.localtime(myLog.open_time)  # type: time.struct_time
		close_t = time.localtime(myLog.close_time)  # type: time.struct_time
		FeedingLog.objects.create(
			box_id=myLog.box_id,
			feeding_id=myLog.feeding_id,
			card_id=myLog.card_id,
			open_time=datetime.datetime(
				open_t.tm_year, open_t.tm_mon, open_t.tm_mday, open_t.tm_hour, open_t.tm_min, open_t.tm_sec,
				tzinfo=datetime.timezone(offset=datetime.timedelta())  # This basically means "UTC == Local Time"
			),
			close_time=datetime.datetime(
				close_t.tm_year, close_t.tm_mon, close_t.tm_mday, close_t.tm_hour, close_t.tm_min, close_t.tm_sec,
				tzinfo=datetime.timezone(offset=datetime.timedelta())  # This basically means "UTC == Local Time"
			),
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
		time_stamp_t = time.localtime(myLog.time_stamp)  # type: time.struct_time
		SystemLog.objects.create(
			time_stamp=datetime.datetime(
				time_stamp_t.tm_year, time_stamp_t.tm_mon, time_stamp_t.tm_mday, time_stamp_t.tm_hour, time_stamp_t.tm_min, time_stamp_t.tm_sec,
				tzinfo=datetime.timezone(offset=datetime.timedelta())  # This basically means "UTC == Local Time"
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
			key names: BrainBox_ID / BrainBox_Name / Sync_Interval
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
		Returns ALL account info: username&password
		"""
		return tuple(Account.objects.all())

	@staticmethod
	def add_account(user:str, password:str):
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
	### Start of FoodBox functions ###
