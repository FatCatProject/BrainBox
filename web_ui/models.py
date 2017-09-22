from django.db import models
from bbox.models import FoodBox


class Card(models.Model):
	card_id = models.TextField(primary_key=True, db_column="card_id")
	card_name = models.TextField(blank=False, default=card_id, db_column="card_name")

	class Meta:
		managed = True
		db_table = "cards"

	def __str__(self):
		return "card_id: {0}, card_name: {1}".format(self.card_id, self.card_name)


class CardOpen(models.Model):
	rowid = models.AutoField(primary_key=True, db_column="rowid")
	card_id = models.ForeignKey(Card, blank=False, db_column="card_id")
	box_id = models.ForeignKey(FoodBox, blank=False, db_column="box_id")
	active = models.BooleanField(default=True, blank=False, db_column="active")
	changed_date = models.DateTimeField(blank=False, db_column="changed_date")

	class Meta:
		managed = True
		db_table = "card_opens"

	def __str__(self):
		return "rowid: {0}, card_id: {1}, box_id: {2}, active: {3}, changed_date: {4}".format(
			self.rowid, self.card_id, self.box_id, self.active, self.changed_date
		)
