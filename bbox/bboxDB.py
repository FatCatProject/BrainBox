import os.path
import sqlite3
import time

from .models import FeedingLog, Account, FoodBox, SystemLog, SystemSettings, MessageTypes


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
	### END of feeding_logs functiones ###
