from django.contrib import admin
from .models import Parent , Evaluator, CustomUser , Profile
from django.contrib.auth.admin import UserAdmin
# Register your models here.

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "password", "phone", "child_name", "child_dob")  # Customize fields visible in the admin panel


@admin.register(Evaluator)
class EvaluatorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "password")  # Customize fields visible in the admin panel



# Define a custom UserAdmin class to modify how the CustomUser is displayed in the admin interface
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff']

# Register the custom user admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)

