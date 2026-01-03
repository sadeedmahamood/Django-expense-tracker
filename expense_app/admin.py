from django.contrib import admin
from .models import User, Expense
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['name','email','phn_no','created_at']
    search_fields = ['email','phn_no']
admin.site.register(User, UserAdmin)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'date']
    search_fields = ['user__name', 'category']
    list_filter = ['category', 'date']
admin.site.register(Expense, ExpenseAdmin)