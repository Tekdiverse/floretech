import resend
import threading
from .models import UserToken
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.shortcuts import render,redirect
from django.http import JsonResponse

resend.api_key = "re_CUsQ9BQT_NM7D9LpoKacpfCMCbfYvTaE3"
def send_email_async(email_data):
    # Send the email using the resend module
    resend.Emails.send(email_data)

def reset_password(request, user):
    # Generate a random token
    token = get_random_string(length=32)
    
    # Create a UserToken instance
    user_token = UserToken.objects.create(
        user=user,
        token=token,
        token_type='password_reset',
        expires_at=timezone.now() + timezone.timedelta(minutes=30)
    )
    
    # Compose the email message
    recipient = user.email
    reset_link = f'https://profitopit.net/reset-password/{token}/'
    email_data = {
                "from": "Profitopit <noreply@profitopit.net>",
                "to": recipient,
                "subject": "FORGOT PASSWORD",
                "html": f"""
                    <!DOCTYPE html>
                    <html lang="en">
                   
                    <body>
                        <div class="container">
                            <td align="center" valign="top" bgcolor="#ffffff" style="border-radius:5px;border-left:1px solid #e0bce7;border-top:1px solid #e0bce7;border-right:1px solid #efefef;border-bottom:1px solid #efefef">
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
          <tbody>
            <tr>
              <td valign="top" align="center" style="font-family:Google Sans,Roboto,Helvetica,Arial sans-serif;font-size:36px;font-weight:500;line-height:44px;color:#202124;padding:40px 40px 0px 40px;letter-spacing:-0.31px">
              <img src="https://www.profitopit.net/static/img/logo-dark.png" style="border-radius: 15px;" height="200"/>
                </td>
            </tr>
            
            <tr>
              <td valign="top" align="center" style="font-family:Google Sans,Roboto,Helvetica,Arial sans-serif;font-size:14px;font-weight:500;height:44px;color:#202124;padding:40px 40px 0px 40px;letter-spacing:-0.31px">
              
                <h2>Hi <span class="il">{user.username}</span>!</h2></td>
            </tr>
            

            
            <tr>
              <td valign="top" align="left" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:40px 40px 20px 40px">
              You requested a password reset on your<br> Profitopit account.</td>
            </tr>
            <tr>
              <td valign="top" align="left" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:40px 40px 20px 40px">
              Please click on this link {reset_link}<br> to reset your password, and set a new password on your account.</td>
            </tr>



        
            <tr>
              <td valign="top" align="cenetr" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:20px 20px 0px 40px">
              
                If you did not initialize this request, please ignore this email. </td>
            </tr>
            <tr>
              <td valign="top" align="center" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:10px 40px 40px 40px">
                <a href="https://profitopit.net">profitopit.net</a></td>
            </tr>
            
          </tbody>
        </table>
      </td>
                        </div>
                    </body>
                    </html>
                """,
            }

            # Create a thread to send the email asynchronously
    email_thread = threading.Thread(target=send_email_async, args=(email_data,))
    email_thread.start()

    
    return JsonResponse({'success': True, 'message': f"Password reset email sent successfully"})