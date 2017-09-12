import sqlite3
import time
import os.path


def create_brainboxDB():
	"""
	Create new DB file and connect to it
	Check if the DB was created successfully
	If not throw exception
	"""
	try:
		conn = sqlite3.connect('brainboxDB.sqlite3')
	except sqlite3.OperationalError:
		pass
	finally:
		# TODO logic
		pass
	# print('Error creating DB')
	c = conn.cursor()
	c.execute("PRAGMA foreign_keys = ON")
	c.execute('CREATE TABLE IF NOT EXISTS system_settings('
			  'key_name TEXT NOT NULL , '
			  'value_text TEXT, '
			  'PRIMARY KEY(`key_name`) );')

	c.execute('CREATE TABLE IF NOT EXISTS system_logs('
			  'time_stamp NUMERIC NOT NULL,'
			  'message TEXT, '
			  'message_type TEXT NOT NULL,'
			  'severity INTEGER NOT NULL);')

	c.execute('CREATE TABLE IF NOT EXISTS feeding_logs('
			  'box_id TEXT NOT NULL ,'
			  'feeding_id TEXT NOT NULL ,'
			  'card_id TEXT NOT NULL,'
			  'open_time NUMERIC NOT NULL,'
			  'close_time NUMERIC NOT NULL,'
			  'start_weight NUMERIC NOT NULL,'
			  'end_weight NUMERIC NOT NULL,'
			  'synced INTEGER NOT NULL,'
			  'PRIMARY KEY(`feeding_id`), '
			  'FOREIGN KEY(`box_id`) REFERENCES `food_boxes` );')

	c.execute('CREATE TABLE IF NOT EXISTS food_boxes('
			  'box_id TEXT NOT NULL ,'
			  'box_ip TEXT NOT NULL ,'
			  'box_name TEXT NOT NULL,'
			  'box_last_sync TEXT NOT NULL,'
			  'PRIMARY KEY(`box_id`));')

	c.execute('CREATE TABLE IF NOT EXISTS account('
			  '`user_name` TEXT NOT NULL , '
			  '`password` TEXT NOT NULL,'
			  'PRIMARY KEY(`user_name`) );')

	conn.commit()
	c.close()
	conn.close()
