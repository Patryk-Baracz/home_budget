from django.db import models

# Create your models here.

class FamilyMember(models.Model):
    name = models.CharField(max_length=100)