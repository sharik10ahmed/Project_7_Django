from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

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
        mobile = request.POST.get('mobile') # Can be saved to a user profile if needed, otherwise ignored for default User
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'FutureStack/register.html')
            
        # Create user
        username = email # Use email as username
        first_name = fullname.split()[0] if fullname else ""
        last_name = " ".join(fullname.split()[1:]) if fullname and len(fullname.split()) > 1 else ""
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            # Log the new user in
            auth_login(request, user)
            messages.success(request, "Account created successfully! Welcome to FutureStack.")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            
    return render(request, 'FutureStack/register.html')

def about_view(request):
    return render(request, 'FutureStack/about.html')

def courses_view(request):
    return render(request, 'FutureStack/courses.html')

def live_classes_view(request):
    return render(request, 'FutureStack/live_classes.html')

def articles_view(request):
    return render(request, 'FutureStack/articles.html')
