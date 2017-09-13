from django.db import models
import datetime
from django.utils import timezone
from enum import Enum


class Account(models.Model):
    user_name = models.TextField(unique=True)
    password = models.TextField()

    class Meta:
        managed = False
        db_table = 'account'


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
        managed = False
        db_table = 'feeding_logs'


class FoodBox(models.Model):
    box_id = models.TextField(unique=True)
    box_ip = models.TextField()
    box_name = models.TextField()
    box_last_sync = models.TextField()

    class Meta:
        managed = False
        db_table = 'food_boxes'


class SystemLog(models.Model):
    time_stamp = models.TextField()  # This field type is a guess.
    message = models.TextField(blank=True, null=True)
    message_type = models.TextField()
    severity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_logs'


class SystemSettings(models.Model):
    key_name = models.TextField(unique=True)
    value_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'system_settings'

class MessageTypes(Enum):
	Information = 1  # General information
	Error = 2  # Something bad happened but operation can continue
	Fatal = 3  # Something bad happened and program has to stop