from django.contrib import admin
from userauths.models import User
from .models import Transaction, Withdraw

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email','total_balance','total_invested','total_deposit','address']

admin.site.register(User, UserAdmin)

# admin.py


admin.site.site_header = 'Profitopit Administration'

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_id','interval_count','converted_days', 'timestamp')
    actions = ['confirm_transactions']
    def confirm_transactions(modeladmin, request, queryset):
        for transaction in queryset:
            # Update related user's fields
            transaction.user.total_deposit += transaction.user.total_invested
            transaction.user.total_invested = 0

            # Set plan_interval_processed to True
            transaction.plan_interval_processed = True

            # Save the changes
            transaction.user.save()
            transaction.save()
            
        modeladmin.message_user(request, f'{queryset.count()} transactions confirmed.')

    confirm_transactions.short_description = "Confirm selected transactions"
    def converted_days(self, obj):
        # Call the convert_description_to_days method on the Transaction instance
        return obj.convert_description_to_days()

    converted_days.short_description = 'Days till expire'

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