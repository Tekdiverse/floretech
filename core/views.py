from django.shortcuts import render,redirect
import django
from django.contrib import messages
from .models import Plan, UserComplaints
from core.forms import ContactForm
from userauths.forms import TransactionForm, WithdrawForm, UserRegisterForm
from userauths.models import Transaction, Deposit, Withdraw
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from userauths.models import User
from django.contrib.auth import login, authenticate
from core.models import BtcAddress,EthAddress,OtherAddress
from django.http import JsonResponse
import resend



def login_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='userauths:sign-in'
):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def custom_error_page(request,exception):
    return render(request, 'errors/custom_error.html')
def custom_error_page2(request,exception):
    return render(request, 'errors/csrf_error.html')
def custom_error_page1(request):
    return render(request, 'errors/500.html')
def index(request):
    plans = Plan.objects.all()
    context = {
        "plan": plans
    }
    return render(request, "core/index.html",context)

def faq(request):
    return render(request,"core/faq.html")
def about(request):
    return render(request,"core/about.html")
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Thanks, message sent succesfully")
            return redirect('core:index')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})

resend.api_key = "re_ZZYtkQ5f_BRYb61sidHksYWwnwrEmZzZt"
@login_required
def dashboard_view(request):
    plans = Plan.objects.all()
    
    context = {
        "plans": plans
    }
    
    return render(request, "core/dashboard-crypto.html", context)


@login_required
def profile_view(request):
    return render(request, "core/pages-profile.html")

@login_required
def withdrawal_view(request):
    user_withdrawals = Withdraw.objects.filter(user=request.user).order_by('-timestamp')
    context = {'user_withdrawals': user_withdrawals}
    return render(request, "core/withdrawals.html", context)
@login_required
def profile_settings_view(request):
    current_user = User.objects.get(id=request.user.id)
    form = UserRegisterForm(request.POST or None, instance=current_user)
    if form.is_valid():
        form.save()
        login(request, current_user)
        messages.success(request, "Profile updated successfully ")
        return redirect("core:dashboard")
    
    return render(request, "core/pages-profile-settings.html", {'form':form})


@login_required
def plans_view(request):
    plans = Plan.objects.all()
    context = {
        "plan": plans
    }
    return render(request, "core/product-list.html", context)


def plan_detail_view(request, pid):
    if request.user.is_authenticated:
        form = TransactionForm()
        product = Plan.objects.get(pid=pid)
        products = Plan.objects.filter().exclude(pid=pid)
        p_image = product.product_image()
    
        context = {
            "form": form,
            "p": product,
            "p_image": p_image,
            "products": products,

        }
    
        return render(request, "core/product-detail.html", context)
    else:
        messages.warning(request, "Sign in to activate plan")
        return redirect("userauths:sign-in")

@login_required
def deposit_view(request):
    btc = BtcAddress.objects.all()
    eth = EthAddress.objects.all()
    other = OtherAddress.objects.all()
    context ={
        'btc': btc,
        'eth': eth,
        'other': other,
    }
    return render(request, "core/deposit.html",context)

@login_required
def send_deposit_review(request):
    user = request.user
    email = request.user.email
    amount = request.POST['deposit']
    wallet_address = request.POST['address']
    trx_hash=request.POST['trx_hash']
    review = Deposit.objects.create(
        user = user,
        amount = request.POST['deposit'],
        currency = request.POST['options'],
        wallet_address = request.POST['address'],
        trx_hash=request.POST['trx_hash'],
    )
    r = resend.Emails.send({
                "from": "Profitopit <support@profitopit.net>",
                "to": 'Profitopitcontantcenter@email.com',
                "subject": "New User",
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
                                margin-top: 20px;.,
                                font-size: 12px;
                                color: #666666;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>Hey Admin,<br> Someone created an account !</h1>
                            <p>{user} with email: {email} has deposited:.</p>
                            <h2>Amount: {amount}</h2>
                            <p>wallet address: {wallet_address}</p>
                            <p>Transaction Hash: {trx_hash}</p><br><br>
                            <div style="text-align: center; align-items: center;">
                                <a href="https://profitopit.net/admin/userauths/deposit/ class="btn btn-primary" target="_blank">Admin Panel</a><br><br>
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
  
    btc = BtcAddress.objects.all()
    eth = EthAddress.objects.all()
    other = OtherAddress.objects.all()
    context ={
        'btc': btc,
        'eth': eth,
        'other': other,
    }

    return render(request, "core/wallet-details.html", context)

@login_required
def referral_view(request):
    current_user = request.user
    current_user_referral_code = current_user.referral_code
    current_user_referrer_code = current_user.referred

    # Count the number of users with the same referral code
    referred_users = User.objects.filter(referred=current_user_referral_code)
    referred_users_count = User.objects.filter(referred=current_user_referral_code).count()

    # Get the users who have the same referral code as the current user
    user_referrer = User.objects.filter(referral_code=current_user_referrer_code)

    context = {
        'current_user': current_user,
        'referred_users': referred_users,
        'referred_users_count': referred_users_count,
        'user_referrer': user_referrer,
    }
    return render(request, "core/referrals.html", context)
@login_required
def send_payment_review(request, pid):
    user = request.user
    plan = Plan.objects.get(pid=pid)
    least_amount = plan.least_amount
    max_amount = plan.max_amount
    amount = Decimal(request.POST['amount'])
    if float(request.POST['amount']) <= user.total_deposit:
        user.total_deposit -= amount
        user.save()
        user.total_invested += amount
        user.save()


        review = Transaction.objects.create(
            user = user,
            title = plan.title,
            interval = plan.interval,
            percentage_return = plan.percentage_return,
            amount = request.POST['amount'],
            least_amount = least_amount,
            max_amount = max_amount,
        )
    else:
        messages.warning(request,"Insufficient Balance, Please Deposit or Choose A Plan")
        return redirect('core:deposit')
    date = review.timestamp
    tid = review.transaction_id
    context = {
        "amount":amount,
        "plan":plan,
        "date": date,
        "tid": tid,
    }

    return render(request,"core/success.html", context)

@login_required
def transaction_view(request):

    user_transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    context = {'user_transactions': user_transactions}
    return render(request, "core/transactions.html", context)


@login_required
def deposits_view(request):

    user_deposits = Deposit.objects.filter(user=request.user).order_by('-timestamp')
    context = {'user_deposits': user_deposits}
    return render(request, "core/deposits.html", context)

@login_required
def withdraw_view(request):
    user = request.user
    email = request.user.email
    if request.method == 'POST':
        currency = request.POST['options']
        wallet_address = request.POST['wallet_address']
        if float(request.POST['amount']) <= user.total_balance:
            amount = Decimal(request.POST['amount'])
            review = Withdraw.objects.create(
                user = user,
                email = email,
                amount = amount,
                currency = currency,
                wallet_address = wallet_address,
            )
            messages.success(request,"Withdrawal placement pending")
            r = resend.Emails.send({
            "from": "Profitopit <support@profitopit.net>",
            "to": 'Profitopitcontantcenter@email.com',
            "subject": "Withdrawal Placement",
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
                            margin-top: 20px;.,
                            font-size: 12px;
                            color: #666666;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Hey Admin,<br> Someone created an account !</h1>
                        <p>A user: {user} with email: {email} has placed a withdrawal of .</p>
                        <h2>{amount}</h2>
                        <p>Login to your admin panel to view them:</p><br><br>
                        <div style="text-align: center; align-items: center;">
                            <a href="https://profitopit.net/admin/userauths/withdraw/" class="btn btn-primary" target="_blank">Admin Panel</a><br><br>
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
  
    
            return redirect('core:dashboard')

        else:
            messages.warning(request,"Insufficient Balance")
            return redirect('core:withdraw')
    else:
        form = WithdrawForm()
    context = {
        'form':form,
        'user': user
        }
    return render(request,"core/withdraw.html",context)

@login_required
def search_view(request):
    query = request.GET.get("search")

    plans = Plan.objects.filter(title__icontains=query).order_by("-date")
    transactions = Transaction.objects.filter(title__icontains=query).order_by("-timestamp")
    context={
        "plans": plans,
        "query": query,
        "transactions": transactions,
    }
    return render(request, "core/search.html", context)