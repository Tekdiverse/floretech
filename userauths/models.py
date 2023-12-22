from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone

# Create your models here.
STATUS = (
    ("daily", "daily"),
    ("weekly", "weekly"),
    ("monthly", "monthly"),
    ("hourly", "hourly"),
)
class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=100)
    total_balance = models.DecimalField(max_digits=1000, decimal_places=2, default="0.00")
    total_invested = models.DecimalField(max_digits=1000, decimal_places=2, default="0.00")
    total_deposit = models.DecimalField(max_digits=1000, decimal_places=2, default="0.00")
    referral_code = ShortUUIDField(unique=True, length=10, max_length=20, prefix="profit", alphabet="abcdefgh12345")
    referred = models.CharField(max_length=20, blank=True)
    contact = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    btc_address = models.CharField(max_length=100, blank=True)
    eth_address = models.CharField(max_length=100, blank=True)
    usdt_address = models.CharField(max_length=100, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    def save(self, *args, **kwargs):
        self.total_balance = Decimal(self.total_deposit) + Decimal(self.total_invested)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username

        



class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default="0.00")
    title = models.CharField(max_length=50, blank=True)
    interval = models.CharField(choices=STATUS, max_length=16, default="daily")
    percentage_return = models.DecimalField(max_digits=1000, decimal_places=2, default="0.00")
    least_amount = models.DecimalField(max_digits=1000, decimal_places=2, default="0.00")
    max_amount = models.DecimalField(max_digits=1000, decimal_places=2, default="0.00")
    transaction_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix="TRX", alphabet="abcdefgh12345")
    timestamp = models.DateTimeField(auto_now_add=True)

class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=25, blank=True)
    wallet_address = models.CharField(max_length=100, blank=True)
    trx_hash = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def confirm_deposit(self):
        if not self.confirmed:
            # Update user's balance first
            self.user.total_deposit += self.amount
            self.user.save()  # Save the user instance first

            # Update deposit confirmation status
            self.confirmed = True
            self.save()



class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=25, blank=True)
    wallet_address = models.CharField(max_length=100, blank=True)
    transaction_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix="WDR", alphabet="ijklmno12345")
    timestamp = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def confirm_withdrawal(self):
        if not self.confirmed:
            # Update user's balance first
            self.user.total_deposit -= self.amount
            self.user.save()  # Save the user instance first

            # Update deposit confirmation status
            self.confirmed = True
            self.save()
    class Meta:
        verbose_name_plural = "Withdrawal Requests"