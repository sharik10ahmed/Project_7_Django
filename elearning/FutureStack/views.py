from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random

def send_html_email(subject, title, greeting, content_body, cta_box, recipient_email):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{subject}</title>
      <style>
        body {{
          margin: 0;
          padding: 0;
          background-color: #f8fafc;
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          color: #1f2937;
        }}
        .wrapper {{
          width: 100%;
          background-color: #f8fafc;
          padding: 40px 0;
        }}
        .card {{
          max-width: 500px;
          margin: 0 auto;
          background-color: #ffffff;
          border-radius: 16px;
          border: 1px solid rgba(0, 64, 224, 0.08);
          box-shadow: 0 10px 30px rgba(0, 16, 64, 0.05);
          overflow: hidden;
        }}
        .header {{
          background: linear-gradient(135deg, #0040e0 0%, #0090f0 100%);
          padding: 35px 20px;
          text-align: center;
        }}
        .logo-text {{
          color: #ffffff;
          font-size: 26px;
          font-weight: 800;
          margin: 0;
          letter-spacing: 0.5px;
        }}
        .logo-sub {{
          color: rgba(255, 255, 255, 0.8);
          font-size: 11px;
          margin: 6px 0 0 0;
          letter-spacing: 1px;
          text-transform: uppercase;
        }}
        .body {{
          padding: 40px 30px;
        }}
        .title {{
          color: #001040;
          font-size: 20px;
          font-weight: 700;
          margin-top: 0;
          margin-bottom: 20px;
        }}
        .greeting {{
          font-size: 16px;
          font-weight: 600;
          color: #001040;
          margin-bottom: 12px;
        }}
        .text {{
          font-size: 15px;
          color: #4b5563;
          line-height: 1.6;
          margin-bottom: 24px;
        }}
        .cta-container {{
          text-align: center;
          margin: 30px 0;
          padding: 24px;
          background: rgba(0, 64, 224, 0.03);
          border: 1px dashed rgba(0, 64, 224, 0.2);
          border-radius: 12px;
        }}
        .cta-label {{
          font-size: 11px;
          color: #0040e0;
          font-weight: 700;
          text-transform: uppercase;
          margin-bottom: 8px;
          letter-spacing: 0.5px;
        }}
        .cta-value {{
          font-size: 32px;
          font-weight: 800;
          color: #001040;
          letter-spacing: 6px;
          margin: 0;
        }}
        .button {{
          display: inline-block;
          padding: 12px 30px;
          background: linear-gradient(135deg, #0040e0 0%, #0090f0 100%);
          color: #ffffff !important;
          text-decoration: none;
          font-weight: 700;
          font-size: 14px;
          border-radius: 99px;
          box-shadow: 0 4px 15px rgba(0, 64, 224, 0.2);
          margin: 10px 0;
        }}
        .footer {{
          padding: 20px 30px 40px 30px;
          text-align: center;
          font-size: 12px;
          color: #9ca3af;
          border-top: 1px solid #f1f5f9;
        }}
        .footer a {{
          color: #0040e0;
          text-decoration: none;
        }}
      </style>
    </head>
    <body>
      <div class="wrapper">
        <div class="card">
          <div class="header">
            <h1 class="logo-text">FutureStack</h1>
            <p class="logo-sub">Integrating talent, thought and action.</p>
          </div>
          <div class="body">
            <h2 class="title">{title}</h2>
            <p class="greeting">{greeting}</p>
            <p class="text">{content_body}</p>
            {cta_box}
          </div>
          <div class="footer">
            <p>&copy; 2026 FutureStack. All rights reserved.</p>
            <p>If you did not request this email, please ignore it.</p>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    send_mail(
        subject,
        "",
        None,
        [recipient_email],
        html_message=html_content,
        fail_silently=False
    )

def home(request):
    return render(request, 'FutureStack/index.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # In Django, standard auth uses username. Let's find user by email.
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = email # Fallback

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            
    return render(request, 'FutureStack/login.html')

def register_view(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'FutureStack/register.html')
            
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        
        # Save to session
        request.session['registration_data'] = {
            'fullname': fullname,
            'email': email,
            'mobile': mobile,
            'password': password,
        }
        request.session['registration_otp'] = otp
        
        # Send OTP using premium HTML template
        subject = "Verify Your Email - FutureStack OTP"
        title = "Email Verification Required"
        greeting = "Hello,"
        content_body = "Thank you for starting your learning evolution with FutureStack! To complete your registration and secure your account, please verify your email address using the one-time passcode (OTP) below."
        cta_box = f"""
        <div class="cta-container">
          <p class="cta-label">Your One-Time Passcode</p>
          <p class="cta-value">{otp}</p>
        </div>
        """
        try:
            send_html_email(subject, title, greeting, content_body, cta_box, email)
            messages.success(request, f"An OTP has been sent to {email}. Please enter it below to verify your email.")
            return redirect('otp_verify')
        except Exception as e:
            messages.error(request, f"Error sending OTP email: {str(e)}")
            return render(request, 'FutureStack/register.html')
            
    return render(request, 'FutureStack/register.html')

def otp_verify_view(request):
    reg_data = request.session.get('registration_data')
    session_otp = request.session.get('registration_otp')
    
    if not reg_data or not session_otp:
        messages.error(request, "Session expired or invalid access. Please register again.")
        return redirect('register')
        
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        if not user_otp:
            messages.error(request, "Please enter the OTP.")
            return render(request, 'FutureStack/otp_verify.html')
            
        if user_otp.strip() == session_otp:
            fullname = reg_data.get('fullname')
            email = reg_data.get('email')
            password = reg_data.get('password')
            mobile = reg_data.get('mobile')
            
            # Create user
            username = email
            first_name = fullname.split()[0] if fullname else ""
            last_name = " ".join(fullname.split()[1:]) if fullname and len(fullname.split()) > 1 else ""
            
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                
                # Log the user in
                auth_login(request, user)
                
                # Send confirmation email using premium HTML template
                subject = "Welcome to FutureStack - Registration Successful"
                title = "Welcome to FutureStack!"
                greeting = f"Hello {fullname or username},"
                content_body = "Congratulations! Your registration at FutureStack was successful. You have officially unlocked a community of thousands of students developing cutting edge skills, accessing live learning environments, and launching global careers."
                cta_box = f"""
                <div style="text-align: center; margin: 30px 0;">
                  <a href="http://127.0.0.1:8000/" class="button">Go to Homepage</a>
                </div>
                """
                send_html_email(subject, title, greeting, content_body, cta_box, email)
                
                # Clear session
                if 'registration_data' in request.session:
                    del request.session['registration_data']
                if 'registration_otp' in request.session:
                    del request.session['registration_otp']
                    
                messages.success(request, f"Welcome to FutureStack, {user.first_name or user.username}!")
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Error creating account: {str(e)}")
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            
    return render(request, 'FutureStack/otp_verify.html', {'email': reg_data.get('email')})

def about_view(request):
    return render(request, 'FutureStack/about.html')

def courses_view(request):
    from .models import Course
    courses = Course.objects.all()
    return render(request, 'FutureStack/courses.html', {'courses': courses})

def live_classes_view(request):
    return render(request, 'FutureStack/live_classes.html')

def articles_view(request):
    return render(request, 'FutureStack/articles.html')

def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

def course_detail_view(request, course_id):
    from django.shortcuts import get_object_or_404
    from .models import Course
    course = get_object_or_404(Course, id=course_id)
    enrolled = request.GET.get('enrolled') == 'true'
    return render(request, 'FutureStack/course_detail.html', {'course': course, 'enrolled': enrolled})

