"""
URL configuration for elearning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from FutureStack.views import home, login_view, register_view, about_view, courses_view, live_classes_view, articles_view, logout_view, otp_verify_view, course_detail_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('verify-otp/', otp_verify_view, name='otp_verify'),
    path('logout/', logout_view, name='logout'),
    path('about/', about_view, name='about'),
    path('courses/', courses_view, name='courses'),
    path('course-detail/<int:course_id>/', course_detail_view, name='course_detail'),
    path('live/', live_classes_view, name='live_classes'),
    path('articles/', articles_view, name='articles'),
]
