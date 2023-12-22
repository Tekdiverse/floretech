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
import secrets
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def generate_reset_token():
    # Generate a URL-safe random token with 32 bytes (256 bits) of entropy
    return secrets.token_urlsafe(32)
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
            resend.api_key = "re_ZZYtkQ5f_BRYb61sidHksYWwnwrEmZzZt"
            html_message = render_to_string('core/email.html')
            plain_message = strip_tags(html_message)
            r = resend.Emails.send({
                "from": "Profitopit <support@profitopit.net>",
                "to": email,
                "subject": "Welcome to Profitopit",
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
                            h1, p {{
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
                            <h1>Hi {username},<br> Thanks for signing up to Profitopit !</h1>
                            <p>We're thrilled to have you join our investment platform. Get ready to explore new opportunities and grow your portfolio.</p>
                            <p>We can tell you're eager to jump into action. Why don't you take a look at our <a href="https://profitopit.net/app/plans" style="color: #007bff;">plans</a> and get familiar with our platform.</p>
                            <p>Take the first step by signing in to your account:</p><br><br>
                            <div style="text-align: center; align-items: center;">
                                <a href="https://profitopit.net/app/dashboard" class="btn btn-primary" target="_blank">Sign In</a><br><br>
                            </div>
                            <p class="disclaimer">
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
                            h1, p {{
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
                            <p>A new user with the name {username} and email {email} signed up to profitopit.</p>
                            <p>Check them out, they can be potential clients</p>
                            <p>Login to your admin panel to view them:</p><br><br>
                            <div style="text-align: center; align-items: center;">
                                <a href="https://profitopit.net/admin/userauths/user/" class="btn btn-primary" target="_blank">Admin Panel</a><br><br>
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
  
            

            # message = EmailMultiAlternatives(
            #     subject='Welcome to Profitopit',
            #     body= plain_message,
            #     from_email='support@profitopit.net',
            #     to=[email]
            # )
            # message.attach_alternative(html_message,"text/html")
            # message.send()

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




@login_required
def get_user_data(request):
    # Retrieve the current user
    current_user = request.user

    # Fetch data for the current user
    data = {
        'total_balance': str(current_user.total_balance),
        'total_invested': str(current_user.total_invested),
        'total_deposit': str(current_user.total_deposit),
        # Add other fields as needed
    }

    return JsonResponse(data)
def logout_view(request):
    logout(request)
    # messages.success(request, "User successfully logged out.")
    return redirect("core:index")

def lock_screen_view(request):
    logout(request)
    return redirect("userauths:sign-in")
