from django.db import models


# Create your models here.
class Section(models.Model):
	name = models.CharField(max_length=64, null=True, unique=True)

	def __str__(self):
		return f"{self.name}"


class Item(models.Model):
	store = models.CharField(max_length=64, null=True)
	name = models.CharField(max_length=100, null=True, unique=True)
	img = models.CharField(max_length=100, null=True)
	price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
	section = models.CharField(max_length=100, null=True)

	def __str__(self):
		return f"{self.name}, Price: {self.price}, From: {self.store}, Section: {self.section}"
