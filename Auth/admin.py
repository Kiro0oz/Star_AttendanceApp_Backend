from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm 


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm 
    
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'committee', 
        'role',       
        'phone_number', 
        'is_staff'
    )
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'university_year')}),
        ('Permissions & Roles', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'committee', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )


    add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('username', 'email', 'role', 'committee', 'phone_number', 'university_year', 'password'), 
            }),
            ('Permissions', {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            }),
        )
        


admin.site.register(User, CustomUserAdmin)