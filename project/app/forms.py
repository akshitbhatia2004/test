from django import forms
from .models import InstituteSignup, Parent, ParentSignup, Evaluator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Import the CustomUser model


# Evaluator Form
class EvaluatorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Evaluator
        fields = "__all__"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

#  Parent Registration Form
class ParentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Parent
        fields = ['email', 'password', 'phone', 'child_name', 'child_dob']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Parent.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# Parent Signup Form
class ParentSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = ParentSignup
        fields = ['parent_name', 'child_name', 'mobile', 'email', 'username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

#  Parent Login Form
class ParentLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

#  Institute Signup Form
class InstituteSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = InstituteSignup
        fields = ['name', 'email', 'username', 'password', 'phone', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  # ✅ Make sure this is present

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('evaluator', 'Evaluator'), ('parent', 'Parent')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")  # ✅ This now works

        return cleaned_data
    


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')

# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

#login


class CustomLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.", code='inactive')

