from django.contrib import admin
from userauths.models import User
from .models import Transaction, Withdraw

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email','total_balance','total_invested','total_deposit','address']

admin.site.register(User, UserAdmin)

# admin.py


admin.site.site_header = 'Profitopit Administration'

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_id', 'timestamp')

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