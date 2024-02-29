from django.contrib import admin
from userauths.models import User
from .models import Transaction, Withdraw
from django.contrib.admin import AdminSite


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email','total_invested','new_field_name1','address']
    def new_field_name1(self, obj):
        return obj.total_deposit
    new_field_name1.short_description = 'Estimated Balance'



admin.site.register(User, UserAdmin)

# admin.py


admin.site.site_header = 'Profitopit Administration'

def confirm_selected_transactions(modeladmin, request, queryset):
    for transaction in queryset:
        transaction.confirm_transactions()

confirm_selected_transactions.short_description = "Confirm selected transactions"

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_id','title','interval_count', 'timestamp', 'expiry_date','confirmed')
    list_filter = ('confirmed',)
    actions = [confirm_selected_transactions]
admin.site.register(Transaction, TransactionAdmin)


def confirm_selected_withdrawals(modeladmin, request, queryset):
    for withdrawal in queryset:
        withdrawal.confirm_withdrawal()

confirm_selected_withdrawals.short_description = "Confirm selected withdrawals"


class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user','currency', 'amount','wallet_address','timestamp','confirmed')
    list_filter = ('confirmed',)
    actions = [confirm_selected_withdrawals]
admin.site.register(Withdraw, WithdrawalAdmin)