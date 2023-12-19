from django.urls import path
from .views import (index, contact_view, dashboard_view, profile_settings_view, 
                    profile_view, plan_detail_view, send_payment_review, 
                    plans_view,deposit_view,send_deposit_review,transaction_view,deposits_view,search_view,withdraw_view,withdrawal_view,faq,about,referral_view)

app_name = "core"

urlpatterns = [
    path('', index, name='index'),
    path('home/', index, name='index'),
    path('contact', contact_view, name='contact'),
    path('faq', faq, name='faq'),
    path('about', about, name='about'),
    path('app/dashboard',dashboard_view, name='dashboard'),
    path('app/dashboard/',dashboard_view, name='dashboard'),
    path('app/deposit',deposit_view, name='deposit'),
    path('app/deposit/payment/',send_deposit_review, name='payment'),
    path('app/deposit/payment',send_deposit_review, name='payment'),
    path('app/profile-settings', profile_settings_view, name='profile-settings'),
    path('app/profile', profile_view, name='profile'),
    path('app/plan/<pid>/', plan_detail_view, name='plan-detail'),
    path('app/plans', plans_view, name='plans'),
    path('app/transactions', transaction_view, name='transactions'),
    path('app/deposits', deposits_view, name='deposits'),
    path('app/referrals', referral_view, name='referrals'),
    path('app/withdraw', withdraw_view, name="withdraw"),
    path('app/withdrawals', withdrawal_view, name="withdrawals"),
    path("send-payment-review/<pid>/", send_payment_review, name="send-payment-review"),
    path('search/', search_view, name='search'),



]
