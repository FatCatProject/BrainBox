from django.db import models
import datetime
from django.utils import timezone
from enum import Enum
import time


class Account(models.Model):
	user_name = models.TextField(unique=True)
	password = models.TextField()

	class Meta:
		managed = True
		db_table = 'account'

	def __str__(self):
		return 'rowid: %d, user_name: %s,  password: %s \n' % \
			   (self.id,
				self.user_name,
				self.password)

class FeedingLog(models.Model):
	box_id = models.TextField()
	feeding_id = models.TextField(unique=True)
	card_id = models.TextField()
	open_time = models.TextField()  # This field type is a guess.
	close_time = models.TextField()  # This field type is a guess.
	start_weight = models.TextField()  # This field type is a guess.
	end_weight = models.TextField()  # This field type is a guess.
	synced = models.IntegerField()

	class Meta:
		managed = True
		db_table = 'feeding_logs'

	def __str__(self):
		return 'rowid: %d ,box_id: %s, feeding uuid: %s,  card: %s,  open time: %s, close time: %s, start weight: %s, end weight: %s, synced: %d \n' % \
			   (self.id,
				self.box_id,
				self.feeding_id,
				self.card_id,
				time.asctime(time.localtime(int(self.open_time))),
				time.asctime(time.localtime(int(self.close_time))),
				self.start_weight,
				self.end_weight,
				self.synced)


class FoodBox(models.Model):
	box_id = models.TextField(unique=True)
	box_ip = models.TextField()
	box_name = models.TextField()
	box_last_sync = models.TextField()

	class Meta:
		managed = True
		db_table = 'food_boxes'

	def __str__(self):
		return 'rowid: %d, box_id: %s,  box_ip: %s,  box_name: %s, box_last_sync: %s \n' % \
			   (self.id,
				self.box_id,
				self.box_ip,
				self.box_name,
				time.asctime(time.localtime(int(self.box_last_sync))),)



class SystemLog(models.Model):
	time_stamp = models.TextField()  # This field type is a guess.
	message = models.TextField(blank=True, null=True)
	message_type = models.TextField()
	severity = models.IntegerField()

	class Meta:
		managed = True
		db_table = 'system_logs'

	def __str__(self):
		return 'rowid: %d, time_stamp: %s,  message: %s,  message_type: %s, severity: %d \n' % \
			   (self.id,
				time.asctime(time.localtime(int(self.time_stamp))),
				self.message,
				self.message_type,
				self.severity)

class SystemSettings(models.Model):
	key_name = models.TextField(unique=True)
	value_text = models.TextField(blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'system_settings'

	def __str__(self):
		return 'rowid: %d, key_name: %s,  value_text: %s \n' % \
			   (self.id,
				self.key_name,
				self.value_text)

class MessageTypes(Enum):
	Information = 1  # General information
	Error = 2  # Something bad happened but operation can continue
	Fatal = 3  # Something bad happened and program has to stop

class SystemSetting(Enum):
	BrainBox_ID = 1  # ID of the BrainBox
	BrainBox_Name = 2  # Name of BrainBox
	Sync_Interval = 3  # Interval between pooling Server
