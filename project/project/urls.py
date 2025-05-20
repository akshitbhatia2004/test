"""
URL configuration for h566 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from app import views
from django.contrib.auth import views as auth_views  # ✅ Fix NameError
from app.views import CustomPasswordResetView  # Replace 'app' with your actual app name
from django.contrib.auth.views import PasswordChangeView


urlpatterns = [
path('admin/', admin.site.urls),
path("", views.index , name="index"),
path('register/', views.register_view, name="register"),
path('login/',views.login_view , name="login"),
path('evaluator/', views.evaluator_register_view , name="evaluator"),
path('parent/',views.parent, name='parent'),
path('nextpage/',views.nextpage, name="nextpage"),
path('successful/',views.successful, name ="successful"),
path('parent_login/',views.parent_login, name="parent_login"),
path('parent-signup/',views.parent_signup, name="parent_signup"),
path('login-successful/',views.login_successful, name="login_successful"),
path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
path('change_password/', PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
path('password_reset/', CustomPasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
path('institutesignup/',views.institute_signup,name ="institute_signup"),
path('institute_Successful/',views.institute_signup_Successful,name="institute_signup_Successful"),
path('base_generic/',views.base_generic, name="base_generic"),
]
