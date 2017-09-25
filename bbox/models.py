from datetime import datetime

from django.db import models


class Account(models.Model):
	user_name = models.TextField(primary_key=True, max_length=20, db_column="user_name")
	password = models.TextField(blank=False, max_length=50, db_column="password")  # TODO - Secure this

	class Meta:
		managed = True
		db_table = 'accounts'

	def __str__(self):
		return "user_name: {0}, password: {1}".format(self.user_name, self.password)


class FoodBox(models.Model):
	box_id = models.TextField(primary_key=True, db_column="box_id")
	box_ip = models.TextField(blank=False, db_column="box_ip")
	box_name = models.TextField(blank=False, db_column="box_name")
	box_last_sync = models.DateTimeField(blank=False, db_column="box_last_synced")

	class Meta:
		managed = True
		db_table = 'food_boxes'

	def __str__(self):
		return "box_id: {0}, box_ip: {1}, box_name: {2}, box_last_sync: {3} \n".format(
			self.box_id, self.box_ip, self.box_name, self.box_last_sync
		)


class Card(models.Model):
	card_id = models.TextField(primary_key=True, db_column="card_id")
	card_name = models.TextField(blank=False, default=card_id, db_column="card_name")
	admin = models.BooleanField(default=False, blank=False, db_column="admin")

	class Meta:
		managed = True
		db_table = "cards"

	def __str__(self):
		return "card_id: {0}, card_name: {1}, admin: {2} \n".format(self.card_id, self.card_name, self.admin)


class CardOpen(models.Model):
	rowid = models.AutoField(primary_key=True, db_column="rowid")
	card_id = models.ForeignKey(Card, blank=False, db_column="card_id", on_delete=models.CASCADE)
	box_id = models.ForeignKey(FoodBox, blank=False, db_column="box_id")
	active = models.BooleanField(default=True, blank=False, db_column="active")
	changed_date = models.DateTimeField(blank=False, db_column="changed_date")

	class Meta:
		managed = True
		db_table = "card_opens"

	def __str__(self):
		return "rowid: {0}, card_id: {1}, box_id: {2}, active: {3}, changed_date: {4} \n".format(
			self.rowid, self.card_id, self.box_id, self.active, self.changed_date
		)

class FeedingLog(models.Model):
	rowid = models.AutoField(primary_key=True, db_column="rowid")
	box_id = models.ForeignKey(FoodBox, blank=False, db_column="box_id")
	feeding_id = models.TextField(blank=False, db_column="feeding_id")
	card_id = models.ForeignKey(Card, blank=False, db_column="card_id")
	open_time = models.DateTimeField(blank=False, db_column="open_time")
	close_time = models.DateTimeField(blank=False, db_column="close_time")
	start_weight = models.FloatField(blank=False, db_column="start_weight")
	end_weight = models.FloatField(blank=False, db_column="end_weight")
	synced = models.BooleanField(blank=False, default=False, db_column="synced")

	class Meta:
		managed = True
		db_table = 'feeding_logs'
		unique_together = ("box_id", "feeding_id")

	def __str__(self):
		return \
			"rowid: {0} ,box_id: {1}, feeding uuid: {2},  card: {3},  open time: {4}, close time: {5}, " \
			"start weight: {6}, end weight: {7}, synced: {8} \n".format(
				self.rowid, self.box_id, self.feeding_id, self.card_id, self.open_time, self.close_time,
				self.start_weight,
				self.end_weight, self.synced
			)


class SystemLog(models.Model):
	rowid = models.AutoField(primary_key=True, db_column="rowid")
	time_stamp = models.DateTimeField(blank=False, db_column="time_stamp")
	message = models.TextField(blank=True, null=True)
	message_type = models.TextField(
		choices=(("Information", "Information"), ("Error", "Error"), ("Fatal", "Fatal"),), blank=False,
		db_column="message_type"
	)
	severity = models.IntegerField(blank=False, db_column="severity")

	class Meta:
		managed = True
		db_table = 'system_logs'

	def __str__(self):
		return "rowid: {0}, time_stamp: {1}, message: {2}, message_type: {3}, severity: {4} \n".format(
			self.rowid, self.time_stamp, self.message, self.message_type, self.severity
		)


class SystemSetting(models.Model):
	key_name = models.TextField(
		primary_key=True, choices=(
			("BrainBox_ID", "BrainBox_ID"), ("BrainBox_Name", "BrainBox_Name"), ("Sync_Interval", "Sync_interval"),
		), db_column="key_name"
	)
	value_text = models.TextField(blank=True, null=True, db_column="value_text")

	class Meta:
		managed = True
		db_table = 'system_settings'

	def __str__(self):
		return "key_name: {0}, value_text: {1} \n".format(
			self.key_name, self.value_text
		)



