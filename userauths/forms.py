import re
import hashlib
from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User,Transaction, Deposit,Withdraw
from .countries import sorted_countries
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from decimal import Decimal
import resend
CURRENCY = (
    ("Bitcoin (BTC)", "Bitcoin (BTC)"),
    ("Ethereum (ETH)", "Ethereum (ETH)"),
    ("Tether (USDT)", "Tether (USDT)"),
)


def validate_referral_code(value):
    """
    Custom validator to check if the referral code exists in the User model.
    If it exists, create the account and add $10 to total_balance.
    If it doesn't exist, raise a ValidationError.
    """
    try:
        user = User.objects.get(referral_code=value)
        user.save()
        # Referral code exists, create account and add $10 to total_balance
        email = user.email
        username = user.username
        resend.api_key = "re_CUsQ9BQT_NM7D9LpoKacpfCMCbfYvTaE3"
        r = resend.Emails.send({
                "from": "Profitopit <support@profitopit.net>",
                "to": email,
                "subject": f"You referred a new user",
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
                            <h1>Hey {username},<br> you have referred a new user !</h1>
                            <p>Referral code: {value}.</p><br>
                            
                            <div style="text-align: center; align-items: center;">
                                <a href="https://profitopit.net/app/referrals" class="btn btn-primary" style="background-color: #007bff; font-size: 16px; border-color: #007bff; padding: 10px 20px; border-radius: 2px;" target="_blank">View Referrals</a><br><br>
                            </div>
                            
                        </div>

                        <!-- Bootstrap JS (Optional, only if you need Bootstrap features) -->
                        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
                        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
                        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
                    </body>
                    </html>
                """,
            })
  
    except User.DoesNotExist:
        raise ValidationError('This referral code does not exist.')

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username","class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"}))
    address = forms.ChoiceField(choices=sorted_countries, widget=forms.Select(attrs={"placeholder": "Country", "class": "form-control"}))
    btc_address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "BTC address", "class": "form-control","id":"password-field"}), required=False)
    eth_address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "ETH address", "class": "form-control","id":"password-field"}), required=False)
    usdt_address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "USDT address", "class": "form-control","id":"password-field"}), required=False)
    referred = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "*Optional","class": "form-control"}),validators=[validate_referral_code], required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control","id":"password-field"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password", "class": "form-control","id":"password-field2"}))
    
    class Meta:
        model = User
        fields = ['username','email','address','btc_address','eth_address','usdt_address','referred']

class TransactionForm(forms.ModelForm):
    user = forms.EmailField(initial='Default Value',widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control",'readonly': 'readonly'}))
    amount = forms.CharField(initial='Default Value',widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control"}))
    least_amount = forms.CharField(initial='Default Value',widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control",'readonly': 'readonly'}))
    max_amount = forms.CharField(initial='Default Value',widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control",'readonly': 'readonly'}))
    transaction_id= forms.CharField(initial='Default Value', widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control",'readonly': 'readonly'}))
    
    class Meta:
        model = Transaction
        fields = ['user','amount','least_amount','max_amount','transaction_id']


class DepositForm(forms.ModelForm):
    user = forms.EmailField(initial='Default Value',widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control",'readonly': 'readonly'}))
    currency = forms.ChoiceField(choices=CURRENCY, widget=forms.Select(attrs={"placeholder": "This question is about..", "class": "form-control","id":"card-holder-input"}))
    wallet_address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Wallet Address", "class": "form-control","id":"card-holder-input","required":True}))
    amount = forms.CharField(initial='Default Value',widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control"}))
    
    class Meta:
        model = Deposit
        fields = ['user','amount','wallet_address','currency']

class WithdrawForm(forms.ModelForm):
    user = forms.CharField(initial='Default Value',widget=forms.TextInput(attrs={"placeholder": "Username","class": "form-control"}))
    email = forms.EmailField(initial='Default Value',widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control",'readonly': 'readonly'}))
    amount = forms.CharField(initial='Default Value',widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control"}))
    currency = forms.ChoiceField(choices=CURRENCY, widget=forms.Select(attrs={"placeholder": "This question is about..", "class": "form-control","id":"card-holder-input"}))
    wallet_address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Wallet Address", "class": "form-control","id":"card-holder-input","required":True}))
    
    class Meta:
        model = Withdraw
        fields = ['user','email','amount','currency','wallet_address']
