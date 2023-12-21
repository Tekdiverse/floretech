from django.shortcuts import render,redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
from userauths.models import User
from django.conf import settings
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
import resend
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def register_view(request):

    form = UserRegisterForm()
    if request.method == "POST":
        address = request.POST['address']
        username = request.POST['username']
        form = UserRegisterForm(request.POST or None)
        
        if form.is_valid():
            
            new_user = form.save()
            
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get('email')
            messages.success(request, f"Hey {username}, account created successfully")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
            )
            # send_activation_email(new_user,request)
            # send_mail(subject='Welcome to Profitopit',
            #           message=f'Welcome to Profitopit {username}',
            #           from_email='profitopit@profitopit.net',
            #           recipient_list=[email]
            # #           )
            resend.api_key = "re_ZZYtkQ5f_BRYb61sidHksYWwnwrEmZzZt"
            html_message = render_to_string('core/email.html')
            plain_message = strip_tags(html_message)
            # r = resend.Emails.send({
            #     "from": "support@profitopit.net",
            #     "to": f"{email}",
            #     "subject": "Welcome to Profitopit",
            #     "html": plain_message,
            # })
            message = EmailMultiAlternatives(
                subject='Welcome to Profitopit',
                body= plain_message,
                from_email='profitopit@profitopit.net',
                to=[email]
            )
            message.attach_alternative(html_message,"text/html")
            message.send()

            login(request, new_user)
            return redirect("core:dashboard")
    context = {
        'form': form,
    }
    return render(request, 'userauths/sign-up.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in.")
                return redirect("core:dashboard")
            else:
                messages.warning(request, "Invalid credentials, create an account.")
        except:
            messages.warning(request, f"User does not exist")


    return render(request, 'userauths/sign-in.html' )


def logout_view(request):
    logout(request)
    # messages.success(request, "User successfully logged out.")
    return redirect("core:index")

def lock_screen_view(request):
    logout(request)
    return redirect("userauths:sign-in")
