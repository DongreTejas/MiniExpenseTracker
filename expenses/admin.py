# Register your models here.
from django.contrib import admin
from .models import Expense

admin.site.register(Expense)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('expense_id', 'category', 'cost','description')