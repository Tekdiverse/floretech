from django.contrib import admin
from userauths.models import User
from .models import Transaction, Withdraw

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email','total_balance','total_invested','total_deposit','address']

admin.site.register(User, UserAdmin)

# admin.py



class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_id', 'timestamp')

admin.site.register(Transaction, TransactionAdmin)


class WithdrawAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'wallet_address', 'currency')

admin.site.register(Withdraw, WithdrawAdmin)