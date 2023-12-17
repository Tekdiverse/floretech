from django.shortcuts import render,redirect
import django
from django.contrib import messages
from .models import Plan, UserComplaints
from core.forms import ContactForm
from userauths.forms import TransactionForm, WithdrawForm
from userauths.models import Transaction, Deposit, Withdraw
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME


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
def custom_error_page1(request):
    return render(request, 'errors/500.html')
def index(request):
    plans = Plan.objects.all()
    context = {
        "plan": plans
    }
    return render(request, "core/index.html",context)



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

    return render(request, "core/pages-profile-settings.html")


@login_required
def plans_view(request):
    plans = Plan.objects.all()
    context = {
        "plan": plans
    }
    return render(request, "core/product-list.html", context)

@login_required
def plan_detail_view(request, pid):
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

@login_required
def deposit_view(request):
    return render(request, "core/deposit.html")

@login_required
def send_deposit_review(request):
    user = request.user
    review = Deposit.objects.create(
        user = user,
        amount = request.POST['deposit'],
        currency = request.POST['options'],
        wallet_address = request.POST['address'],
    )
    return render(request, "core/wallet-details.html")

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
    if request.method == 'POST':
        if float(request.POST['amount']) <= user.total_balance:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Withdrawal placement pending")
                return redirect('core:dashboard')
            else:
                messages.warning(request,"Invalid Address")
                return redirect('core:withdraw')
        else:
            messages.warning(request,"Insufficient Balance")
            return redirect('core:withdraw')
    else:
        form = WithdrawForm()
    return render(request,"core/withdraw.html",{'form':form})

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