from django.contrib import admin
from expenses.models import *



# Register your models here.
admin.site.site_header = "expense tracker"
admin.site.site_title ="expense tracker"
admin.site.site_url="track your expenses"
admin.site.register(CurrentBalance)


class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display= [
    "description",
    "amount",
    "current_balance",
    "expense_type",
    "created_at",
    "updated_at"
    ]
    search_fields = ["expense_type","description"]
    list_filter = ["expense_type", "description"]
    ordering = ["-updated_at"]
    
admin.site.register(TrackingExpenses,TrackingHistoryAdmin)