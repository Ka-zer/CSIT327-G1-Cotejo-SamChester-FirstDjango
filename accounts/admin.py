from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['last_name','first_name','username', 'email', 'role','is_staff']

    fieldsets = UserAdmin.fieldsets + (
        ("School profile", {"fields": ("role", "course")}),
    ) 