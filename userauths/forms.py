import re
import hashlib
from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User,Transaction, Deposit,Withdraw
from .countries import sorted_countries
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from decimal import Decimal
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
        user.total_deposit += Decimal('10.00')
        user.save()
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
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password", "class": "form-control","id":"password-field"}))
    
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
