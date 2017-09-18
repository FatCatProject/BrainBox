import os.path
import sqlite3
import time

from .models import FeedingLog, Account, FoodBox, SystemLog, SystemSettings, MessageTypes, SystemSetting


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
		self.c.execute('SELECT * FROM feeding_logs WHERE feeding_id = ?', (logID,))
		logData = self.c.fetchall()
		myLog = FeedingLog()
		myLog.id = logData[0][0]
		myLog.box_id = logData[0][1]
		myLog.feeding_id = logData[0][2]
		myLog.card_id = logData[0][3]
		myLog.open_time = logData[0][4]
		myLog.close_time = logData[0][5]
		myLog.start_weight = logData[0][6]
		myLog.end_weight = logData[0][7]
		myLog.synced = logData[0][8]
		return myLog

	def get_all_feeding_logs(self):
		"""
		Returns a tuple of all feeding logs
		"""
		self.c.execute('SELECT * FROM feeding_logs')
		logData = self.c.fetchall()
		logs = []
		for row in logData:
			myLog = FeedingLog()
			myLog.id = row[0]
			myLog.box_id = row[1]
			myLog.feeding_id = row[2]
			myLog.card_id = row[3]
			myLog.open_time = row[4]
			myLog.close_time = row[5]
			myLog.start_weight = row[6]
			myLog.end_weight = row[7]
			myLog.synced = row[8]
			logs.append(myLog)
		return tuple(logs)

	def get_synced_feeding_logs(self):
		"""
		Returns a tuple of synced feeding logs
		"""
		self.c.execute('SELECT * FROM feeding_logs WHERE synced=1')
		logData = self.c.fetchall()
		logs = []
		for row in logData:
			myLog = FeedingLog()
			myLog.id = row[0]
			myLog.box_id = row[1]
			myLog.feeding_id = row[2]
			myLog.card_id = row[3]
			myLog.open_time = row[4]
			myLog.close_time = row[5]
			myLog.start_weight = row[6]
			myLog.end_weight = row[7]
			myLog.synced = row[8]
			logs.append(myLog)
		return tuple(logs)

	def get_not_synced_feeding_logs(self):
		"""
		Returns a tuple of synced feeding logs
		"""
		self.c.execute('SELECT * FROM feeding_logs WHERE synced=0')
		logData = self.c.fetchall()
		logs = []
		for row in logData:
			myLog = FeedingLog()
			myLog.id = row[0]
			myLog.box_id = row[1]
			myLog.feeding_id = row[2]
			myLog.card_id = row[3]
			myLog.open_time = row[4]
			myLog.close_time = row[5]
			myLog.start_weight = row[6]
			myLog.end_weight = row[7]
			myLog.synced = row[8]
			logs.append(myLog)
		return tuple(logs)

	def set_feeding_log_synced(self, myLogUID: str):
		"""
		Get feeding_log UID and change the synced status to True = 1
		"""
		self.c.execute('UPDATE feeding_logs SET synced = 1 WHERE feeding_id = ?', (myLogUID,))
		self.conn.commit()

	def set_feeding_log_not_synced(self, myLogUID: str):
		"""
		Get feeding_log UID and change the synced status to False = 0
		"""
		self.c.execute('UPDATE feeding_logs SET synced = 0 WHERE feeding_id = ?', (myLogUID,))
		self.conn.commit()

	def delete_synced_feeding_logs(self):
		"""
		Delete all synced feeding_logs from the DB
		"""
		self.c.execute('DELETE FROM feeding_logs WHERE synced = 1')
		self.conn.commit()

	def add_feeding_log(self, myLog: FeedingLog):
		"""
		//TODO  fix box_id
		Getting a feeding_log as an object and Adding it to the DB
		"""
		self.c.execute(
			'INSERT INTO feeding_logs (box_id, feeding_id, card_id, open_time, close_time, start_weight, end_weight, synced)'
			' VALUES (?, ?, ?, ?, ?, ?, ?, ?);', (
				"x", myLog.feeding_id, myLog.card_id, myLog.open_time,
				myLog.close_time, myLog.start_weight, myLog.end_weight,
				myLog.synced))
		self.conn.commit()

	### END of feeding_logs functiones ###

	### Start of system_logs functions ###
	def get_system_log_by_id(self, logID: int):
		"""Function gets a SystemLog ID and returns a SystemLog object or None if no such object
		:arg logID: SystemLog ID
		:type logID: int
		:return ret_log: The requested log or None
		:rtype ret_log: Union[SystemLog, None]
		"""
		ret_log = SystemLog()  # type: SystemLog
		self.c.execute(
			'SELECT rowid, time_stamp, message, message_type, severity FROM system_logs WHERE rowid = {}'.format(
				logID))
		data = self.c.fetchone()
		if len(data) == 0:
			return ret_log
		ret_log.id = data[0]
		ret_log.time_stamp = int(data[1])  # type: int  # type: int
		ret_log.message = data[2]  # type: str
		ret_log.message_type = MessageTypes[data[3]]  # type: MessageTypes
		ret_log.severity = data[4]  # type: int
		return ret_log

	def get_all_system_logs(self, logs_since: time.struct_time = None):
		"""Returns a tuple of all system logs since logs_since, or all of them
		:arg logs_since: Limit logs to a date, if it's None then no limit on date.
		:type logs_since: Union[None, time.struct_time]
		:return systemlog_tuple: A tuple of SystemLogs
		:rtype systemlog_tuple: Tuple[SystemLog]
		"""
		log_list = []  # type: List[SystemLog]
		if logs_since is None:
			self.c.execute('SELECT rowid, time_stamp, message, message_type, severity FROM system_logs')
		else:
			self.c.execute(
				'SELECT rowid, time_stamp, message, message_type, severity FROM system_logs WHERE time_stamp >= {0}'.format(
					time.mktime(logs_since)))

		logs_data = self.c.fetchall()
		for data in logs_data:
			myLog = SystemLog()
			myLog.id = data[0]
			myLog.time_stamp = int(data[1])  # type: int  # type: int
			myLog.message = data[2]  # type: str
			myLog.message_type = MessageTypes[data[3]]  # type: MessageTypes
			myLog.severity = data[4]  # type: int
			log_list.append(myLog)
		return tuple(log_list)

	def add_system_log(self, myLog: SystemLog):
		"""Function gets a SystemLog object and writes it to the database
		:arg myLog: The SystemLog to write to the database
		:type myLog: SystemLog
		:return log_rowid: rowid if log was written successfully or None if not
		:rtype log_rowid: Union[int, None]
		"""
		log_rowid = None  # type: int
		self.c.execute('INSERT INTO system_logs (time_stamp, message, message_type, severity) VALUES('
					   '{0}, \'{1}\', \'{2}\', {3})'.format(myLog.time_stamp,
															myLog.message,
															myLog.message_type.name,
															myLog.severity))
		log_rowid = self.c.lastrowid
		print(log_rowid)
		self.conn.commit()
		return False

	### End of system_logs functions ###

	### Start of system_settings functiones ###
	def get_system_setting(self, setting: SystemSetting):
		"""Function returns a value of a specific setting from enums that are available:
			the input must be "SystemSettings.key_name"
			key names: BrainBox_ID / BrainBox_Name / Sync_Interval
			If the key_name is still not written in the DB or has no value it returns None
		"""
		self.c.execute('SELECT * FROM system_settings WHERE key_name = ?', (setting.name,))
		data = self.c.fetchall()
		if len(data) <= 0:
			return None
		else:
			for row in data:
				if row[1] == setting.name:
					return row[2]

	def set_system_setting(self, setting: SystemSetting, value: str):
		"""
		Function sets a value to a key in "system_settings" table
		If the key doesn't exist yet , it will write a new row with the key and value
		"""
		self.c.execute('UPDATE system_settings SET value_text = ? WHERE key_name = ?',
					   (value, setting.name))
		self.conn.commit()
		if self.c.rowcount <= 0:
			self.c.execute('INSERT INTO system_settings (key_name, value_text) VALUES (?, ?)',
						   (setting.name, value))
			self.conn.commit()

	### END of system_logs functions ###

	### Start of Account functions ###
	def get_account_info(self):
		"""
		Returns ALL accounts info: username&password
		"""
		account = Account()
		self.c.execute('SELECT * FROM account')
		data = self.c.fetchall()
		accounts = []
		if len(data) == 0:
			return account
		else:
			for row in data:
				account = Account()
				account.id = row[0]
				account.user_name = row[1]
				account.password = row[2]
				accounts.append(account)
			return tuple(accounts)


	def add_account(self, account: Account):
		"""
		add a new account to DB
		"""
		self.c.execute(
			'INSERT INTO account (user_name, password)'
			' VALUES (?, ?);', (
				account.user_name,
				account.password))
		self.conn.commit()

	def change_user_name_and_or_password(self, acc: Account, new_user_name:str = None, new_password:str = None ):
		"""
		Function receives an account and changes user_name and/or password
		"""
		currentAccount = acc
		if new_user_name is not None:
			self.c.execute('UPDATE account SET user_name = ? WHERE rowid = ?',
						   (new_user_name, currentAccount.id))
			self.conn.commit()
		if new_password is not None:
			self.c.execute('UPDATE account SET password = ? WHERE rowid = ?',
						   (new_password, currentAccount.id))
			self.conn.commit()

### END of Account functions ###

#//Todo FoodBox functions