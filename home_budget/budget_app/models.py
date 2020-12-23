from django.db import models
import datetime
from django.utils.timezone import now

# Create your models here.

class FamilyMember(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class MoneyTransfer(models.Model):
    date = models.DateField(default=datetime.date.today)
    owner = models.ForeignKey(FamilyMember, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)