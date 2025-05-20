from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model 
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import ObjectDoesNotExist
from .models import Assessment
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import (
    EvaluatorForm, ParentRegistrationForm,
    ParentSignupForm, ParentLoginForm, InstituteSignupForm , CustomUserCreationForm

)






from .models import Profile  # If you're using a Profile model

User = get_user_model()  # Custom user model

# Home Page
def index(request):
    return render(request, "index.html")

# Register View


User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # ✅ Send confirmation email
            subject = "Welcome to Our Platform!"
            message = f"Hi {user.username},\n\nThank you for registering with us as a {user.role}."
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, "Registration successful. Confirmation email sent.")
            except Exception as e:
                messages.warning(request, f"User registered, but email failed to send: {e}")

            login(request, user)
            return redirect('login')  # Redirect to login or dashboard
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


# Login View


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST.get('role')  # Coming from dropdown/select in HTML

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # ✅ Access role directly from user if CustomUser is correctly set
            user_role = getattr(user, 'role', None)

            if not user_role:
                messages.error(request, "User role not set.")
                return redirect('login')

            if user_role != role:
                messages.error(request, f"You are not registered as '{role}'.")
                return redirect('login')

            login(request, user)
            request.session['role'] = user_role

            messages.success(request, f'Welcome {username} ({user_role})!')

            # ✅ Redirect based on role
            if user_role == 'parent':
                return redirect('parent')
            elif user_role == 'evaluator':
                return redirect('evaluator')
            elif user_role == 'institute':
                return redirect('institute')
            else:
                return redirect('index')

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

# Logout View


@login_required
def logout_view(request):
    logout(request)
    return redirect("index")


#  Parent Registration
def parent(request):
    if request.method == "POST":
        form = ParentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("successful")
    else:
        form = ParentRegistrationForm()
    return render(request, "parent.html", {"form": form})

#  Parent Login View
def parent_login(request):
    form = ParentLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "parent-login.html", {"form": form, "error": "Invalid credentials."})

    return render(request, "parent-login.html", {"form": form})

#  Parent Signup View
def parent_signup(request):
    if request.method == "POST":
        form = ParentSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
            return redirect("parent_login")
    else:
        form = ParentSignupForm()
    return render(request, "parent-signup.html", {"form": form})

#  Password Reset View
class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        try:
            User.objects.get(email=email)
            return super().form_valid(form)
        except ObjectDoesNotExist:
            return render(self.request, "password_reset.html", {"form": form, "error": "Email not found."})

#  Evaluator Registration
def evaluator_register_view(request):
    if request.method == "POST":
        form = EvaluatorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("nextpage")
    else:
        form = EvaluatorForm()
    return render(request, "evaluator.html", {"form": form})

#  Assessment Graph View
@login_required
def assessment_graph_view(request):
    try:
        assessment = Assessment.objects.get(child_id=request.user.id)
        return render(request, "graph.html", {"score": assessment.score})
    except Assessment.DoesNotExist:
        return render(request, "graph.html", {"error_message": "No assessment found."})

#  Password Change View
@login_required
def change_password(request):
    error_message = None

    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not request.user.check_password(old_password):
            error_message = "Current password is incorrect."
        elif new_password != confirm_password:
            error_message = "New passwords do not match."
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            return redirect("password_successful")

    return render(request, "change_password.html", {"error_message": error_message})

#  Misc Pages
def successful(request):
    return render(request, "successful.html")

def nextpage(request):
    return render(request, "nextpage.html")

def login_successful(request):
    return render(request, "login-successful.html")

def institute_signup(request):
    if request.method == "POST":
        form = InstituteSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("institute_dashboard")
    else:
        form = InstituteSignupForm()
    return render(request, "institute-signup.html", {"form": form})

def institute_signup_Successful(request):
    return render(request, "institute-signup-successful.html")

def base_generic(request):
    return render(request, "base_generic.html")