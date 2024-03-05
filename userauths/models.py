from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
import resend
import re
from django.db import transaction as ts
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
    # total_balance = models.DecimalField(max_digits=1000, decimal_places=2, default="0.00")
    total_invested = models.DecimalField(max_digits=1000, decimal_places=2, default="0.00")
    total_deposit = models.DecimalField(max_digits=1000, decimal_places=2, default="0.00")
    referral_code = ShortUUIDField(unique=True, length=10, max_length=20, prefix="profit", alphabet="abcdefgh12345")
    referred = models.CharField(max_length=20, blank=True)
    contact = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    ref_bonus = models.DecimalField(max_digits=1000, decimal_places=2, default="0.00")
    btc_address = models.CharField(max_length=100, blank=True)
    eth_address = models.CharField(max_length=100, blank=True)
    usdt_address = models.CharField(max_length=100, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    def save(self, *args, **kwargs):
        # self.total_balance = Decimal(self.total_deposit) + Decimal(self.total_invested)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = "Profitopit User"
        



class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default="0.00")
    title = models.CharField(max_length=50, blank=True)
    interval = models.CharField(choices=STATUS, max_length=16, default="daily")
    percentage_return = models.DecimalField(max_digits=100, decimal_places=2, default="0.00")
    least_amount = models.DecimalField(max_digits=1000, decimal_places=2, default="0.00")
    description = models.TextField(null=True, blank=True)
    max_amount = models.DecimalField(max_digits=100, decimal_places=2, default="0.00")
    transaction_id = ShortUUIDField(unique=True, length=20, max_length=30, prefix="TRX", alphabet="abcdefgh12345")
    timestamp = models.DateTimeField(auto_now_add=True)
    plan_interval_processed = models.BooleanField(default=False)
    interval_count = models.IntegerField(default=0)
    days_count = models.IntegerField(default=1)
    expiry_date = models.DateTimeField(default=timezone.now() + timedelta(days=7))
    confirmed = models.BooleanField(default=False)
    
    def confirm_transactions(self):
        if not self.confirmed:
            
            self.user.refresh_from_db()
            self.user.total_deposit -= Decimal(self.amount)
            self.user.save(update_fields=['total_deposit'])

            

            self.user.total_invested += Decimal(self.amount)
            self.user.save(update_fields=['total_invested'])
            
            # Update transaction confirmation status
            self.confirmed = True
            self.save()
            r = resend.Emails.send({
                    "from": "Profitopit <support@profitopit.net>",
                    "to": self.user.email,
                    "subject": "Successful Investment",
                    "html": f"""
                        <!DOCTYPE html>
                        <html lang="en">
                        <body>
                            <div class="container">
                                <h1>Hi {self.user},</h1>
                                <h2>You successfully invested ${self.amount} in the {self.title}</h2>
                                <p>Dear {self.user}, your decision to invest with us speaks volumes, and we're excited to embark on this journey together. Our team is committed to ensuring your experience is nothing short of exceptional.</p>
                                <p>If you have any questions or if there's anything we can assist you with, please feel free to reach out to our customer support team at <a href="mailto:support@profitopit.net">support@profitopit.net</a>. We are here to help and provide any information you may need</p>
                                <p>Once again, thank you for choosing Profitopit. We look forward to a prosperous and successful investment journey together.</p><br><br>
                                <div style="text-align: center; align-items: center;">
                                    <a href="https://profitopit.net/app/dashboard" class="btn btn-primary" style="background-color: #007bff; font-size: 16px; border-color: #007bff; padding: 10px 20px; color: #fff; border-radius: 2px;" target="_blank">Dashboard</a><br><br>
                                </div>
                                
                            </div>
                        </body>
                        </html>
                    """,
                })
            try:
                user = User.objects.get(referral_code=self.user.referred)
                investment_referral_payment = self.user.total_invested * Decimal(0.1)
                user.total_deposit += Decimal(investment_referral_payment)
                user.ref_bonus += Decimal(investment_referral_payment)
                user.save()
            except User.DoesNotExist:
                pass  # Handle the case where the referral user does not exist
            except Exception as e:
                print(e)
    def convert_description_to_days(self):
        match = re.match(r'(\d+) wks? and (\d+) days?', self.description)

        if match:
            weeks, days = map(int, match.groups())
            total_days = weeks * 7 + days
            return total_days
        else:
            match = re.match(r'(\d+) days?', self.description)
            if match:
                days = int(match.group(1))
                return days
            else:
                return 7

    def save(self, *args, **kwargs):
        if self.expiry_date:
            days_to_add = self.convert_description_to_days()
            self.expiry_date = timezone.now() + timezone.timedelta(days=days_to_add)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Users that invested"







class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=25, blank=True)
    wallet_address = models.CharField(max_length=100, blank=True)
    trx_hash = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Users Deposit"
    def confirm_deposit(self):
        if not self.confirmed:
            # Update user's balance first
            self.user.total_deposit += self.amount
            self.user.save()  # Save the user instance first

            # Update deposit confirmation status
            self.confirmed = True
            self.save()
            resend.api_key = "re_CUsQ9BQT_NM7D9LpoKacpfCMCbfYvTaE3"
            r = resend.Emails.send({
                "from": "Profitopit <support@profitopit.net>",
                "to": self.user.email,
                "subject": f"Deposit has been confirmed",
                "html": f"""
                    <!DOCTYPE html>
                    <html lang="en">
                    
                    <body>
                        <div class="container">
                            <h1>Hey {self.user.username},<br> </h1>
                            <h2>Your deposit of ${self.amount} has been confirmed.</h2>
                            <p>The deposit that you made at {self.timestamp} UTC has been confirmed, you can go over to your dashboard to view or invest in any of our plans.</p><br>
                            <div style="text-align: center; align-items: center;">
                                <a href="https://profitopit.net/app/dashboard" class="btn btn-primary" style="background-color: #007bff; font-size: 16px; border-color: #007bff; padding: 10px 20px; border-radius: 2px;" target="_blank">View Dashboard</a><br><br>
                            </div>
                            <p style="margin-top: 20px; font-size: 12px; color: #666666;">
                                Note: This email is sent as part of Profitopit communication. If you believe this is a mistake or received this email in error, please disregard it.
                            </p>
                        </div>

                    </body>
                    </html>
                """,
            })
            referred_user = User.objects.filter(referral_code=self.user.referred).first()

            if referred_user:
                referred_user_email = referred_user.email
                referred_user_username = referred_user.username
                # Calculate the bonus amount (10% of the deposit)
                bonus_amount = self.amount * Decimal(0.1)

                # Update referred user's total_deposit and total_balance
                referred_user.total_deposit += bonus_amount
                referred_user.save()
                r = resend.Emails.send({
                    "from": "Profitopit <support@profitopit.net>",
                    "to": referred_user_email,
                    "subject": f"Your Referral Deposited",
                    "html": f"""
                        <!DOCTYPE html>
                        <html lang="en">
                       
                        <body>
                            <div class="container">
                                <h1>Hey {referred_user_username},<br> </h1>
                                <h2>Your referral made a deposit of ${self.amount}.</h2>
                                <p>A referral bonus of ${bonus_amount} has been credited to your balance.</p><br>
                                <div style="text-align: center; align-items: center;">
                                    <a href="https://profitopit.net/app/dashboard" class="btn btn-primary" style="background-color: #007bff; font-size: 16px; border-color: #007bff; padding: 10px 20px; border-radius: 2px;" target="_blank">View Dashboard</a><br><br>
                                </div>
                                <p style="margin-top: 20px; font-size: 12px; color: #666666;">
                                    Note: This email is sent as part of Profitopit communication. If you believe this is a mistake or received this email in error, please disregard it.
                                </p>
                            </div>

                 
                        </body>
                        </html>
                    """,
                })

 



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
            resend.api_key = "re_CUsQ9BQT_NM7D9LpoKacpfCMCbfYvTaE3"
            r = resend.Emails.send({
                "from": "Profitopit <support@profitopit.net>",
                "to": self.user.email,
                "subject": f"Withdrawal has been confirmed",
                "html": f"""
                    <!DOCTYPE html>
                    <html lang="en">
                  
                    <body>
                        <div class="container">
                            <h1>Hey {self.user.username},<br> </h1>
                            <h2>Your withdrawal of ${self.amount} has been confirmed.</h2><br>
                            <p>The withdrawal you placed at {self.timestamp} UTC has been confirmed, you will be credited to your wallet address shortly.</p><br>
                            <div style="text-align: center; align-items: center;">
                                <a href="https://profitopit.net/app/dashboard class="btn btn-primary" style="background-color: #007bff; font-size: 16px; border-color: #007bff; padding: 10px 20px; border-radius: 2px;" target="_blank">View dashboard</a><br><br>
                            </div>
                            <p style="margin-top: 20px; font-size: 12px; color: #666666;">
                                Note: This email is sent as part of Profitopit communication. If you believe this is a mistake or received this email in error, please disregard it.
                            </p>
                        </div>

                    </body>
                    </html>
                """,
            })
 
    class Meta:
        verbose_name_plural = "Withdrawal Requests"


class UserToken(models.Model):
    TOKEN_TYPES = (
        ('email_confirmation', 'Email Confirmation'),
        ('password_reset', 'Password Reset'),
        ('refresh_token', 'Refresh token'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=20, choices=TOKEN_TYPES)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User Token'
        verbose_name_plural = 'User Tokens'

    def __str__(self):
        return f'Token: {self.token} - Type: {self.token_type}'

    def save(self, *args, **kwargs):
        # Set expiration time to 30 minutes from the current time
        self.expires_at = self.created_at + timezone.timedelta(days=1)
        super().save(*args, **kwargs)