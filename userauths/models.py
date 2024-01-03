from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
import resend
import time
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
    class Meta:
        verbose_name = "Profitopit User"
        



class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default="0.00")
    title = models.CharField(max_length=50, blank=True)
    interval = models.CharField(choices=STATUS, max_length=16, default="daily")
    percentage_return = models.DecimalField(max_digits=1000, decimal_places=2, default="0.00")
    least_amount = models.DecimalField(max_digits=1000, decimal_places=2, default="0.00")
    description = models.TextField(null=True, blank=True)
    max_amount = models.DecimalField(max_digits=1000, decimal_places=2, default="0.00")
    transaction_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix="TRX", alphabet="abcdefgh12345")
    timestamp = models.DateTimeField(auto_now_add=True)
    interval_count = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = "Users that invested"



# Run the task every day
# while True:
#     # Get the current time
#     current_time = time.localtime()

#     # Check if it's a new day (midnight)
#     if current_time.tm_hour == 0 and current_time.tm_min == 0:
#         perform_daily_task()

#     # Wait for a certain period before checking again (adjust as needed)
#     time.sleep(60)  # Check every minute




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
            resend.api_key = "re_ZZYtkQ5f_BRYb61sidHksYWwnwrEmZzZt"
            r = resend.Emails.send({
                "from": "Profitopit <support@profitopit.net>",
                "to": self.user.email,
                "subject": f"Deposit has been confirmed",
                "html": f"""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Welcome to Profitopit</title>
                        <!-- Bootstrap CSS -->
                        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
                        <link rel="preconnect" href="https://fonts.googleapis.com">
                        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                        <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
                        <style>
                            body {{
                                font-family: 'Poppins', sans-serif;
                                background-color: #f5f5f5;
                                margin: 0;
                                padding: 0;
                            }}
                            .container {{
                                max-width: 600px;
                                margin: 20px auto;
                                padding: 20px;
                                background-color: #ffffff;
                                border-radius: 8px;
                                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                            }}
                            h1,h2, p {{
                                color: #333333;
                            }}
                            .btn-primary {{
                                background-color: #007bff;
                                border-color: #007bff;
                                padding: 10px 20px;
                                font-size: 16px;
                                border-radius: 2px;
                            }}
                            .btn-primary:hover {{
                                background-color: #0056b3;
                                border-color: #0056b3;
                            }}
                            a {{
                                color: #fff;
                                text-decoration: none;
                            }}
                            a:hover {{
                                color: #fff;
                            }}
                            .disclaimer {{
                                margin-top: 20px;
                                font-size: 12px;
                                color: #666666;
                            }}
                        </style>
                    </head>
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

                        <!-- Bootstrap JS (Optional, only if you need Bootstrap features) -->
                        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
                        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
                        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
                    </body>
                    </html>
                """,
            })
            referred_user = User.objects.filter(referral_code=self.user.referred).first()

            if referred_user:
                referred_user_email = referred_user.email
                referred_user_username = referred_user.username
                # Calculate the bonus amount (10% of the deposit)
                bonus_amount = self.amount * 0.1

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
                        <head>
                            <meta charset="UTF-8">
                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Welcome to Profitopit</title>
                            <!-- Bootstrap CSS -->
                            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
                            <link rel="preconnect" href="https://fonts.googleapis.com">
                            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                            <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
                            <style>
                                body {{
                                    font-family: 'Poppins', sans-serif;
                                    background-color: #f5f5f5;
                                    margin: 0;
                                    padding: 0;
                                }}
                                .container {{
                                    max-width: 600px;
                                    margin: 20px auto;
                                    padding: 20px;
                                    background-color: #ffffff;
                                    border-radius: 8px;
                                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                                }}
                                h1,h2, p {{
                                    color: #333333;
                                }}
                                .btn-primary {{
                                    background-color: #007bff;
                                    border-color: #007bff;
                                    padding: 10px 20px;
                                    font-size: 16px;
                                    border-radius: 2px;
                                }}
                                .btn-primary:hover {{
                                    background-color: #0056b3;
                                    border-color: #0056b3;
                                }}
                                a {{
                                    color: #fff;
                                    text-decoration: none;
                                }}
                                a:hover {{
                                    color: #fff;
                                }}
                                .disclaimer {{
                                    margin-top: 20px;
                                    font-size: 12px;
                                    color: #666666;
                                }}
                            </style>
                        </head>
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

                            <!-- Bootstrap JS (Optional, only if you need Bootstrap features) -->
                            <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
                            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
                            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
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
            resend.api_key = "re_ZZYtkQ5f_BRYb61sidHksYWwnwrEmZzZt"
            r = resend.Emails.send({
                "from": "Profitopit <support@profitopit.net>",
                "to": self.user.email,
                "subject": f"Withdrawal has been confirmed",
                "html": f"""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Welcome to Profitopit</title>
                        <!-- Bootstrap CSS -->
                        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
                        <link rel="preconnect" href="https://fonts.googleapis.com">
                        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                        <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
                        <style>
                            body {{
                                font-family: 'Poppins', sans-serif;
                                background-color: #f5f5f5;
                                margin: 0;
                                padding: 0;
                            }}
                            .container {{
                                max-width: 600px;
                                margin: 20px auto;
                                padding: 20px;
                                background-color: #ffffff;
                                border-radius: 8px;
                                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                            }}
                            h1,h2, p {{
                                color: #333333;
                            }}
                            .btn-primary {{
                                background-color: #007bff;
                                border-color: #007bff;
                                padding: 10px 20px;
                                font-size: 16px;
                                border-radius: 2px;
                            }}
                            .btn-primary:hover {{
                                background-color: #0056b3;
                                border-color: #0056b3;
                            }}
                            a {{
                                color: #fff;
                                text-decoration: none;
                            }}
                            a:hover {{
                                color: #fff;
                            }}
                            .disclaimer {{
                                margin-top: 20px;
                                font-size: 12px;
                                color: #666666;
                            }}
                        </style>
                    </head>
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

                        <!-- Bootstrap JS (Optional, only if you need Bootstrap features) -->
                        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
                        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
                        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
                    </body>
                    </html>
                """,
            })
 
    class Meta:
        verbose_name_plural = "Withdrawal Requests"