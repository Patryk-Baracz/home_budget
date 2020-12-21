from django.contrib import admin
from budget_app.models import MoneyTransfer, Category

# Register your models here.
admin.site.register(MoneyTransfer)
admin.site.register(Category)
