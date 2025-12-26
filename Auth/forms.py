from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import ROLE_CHOICES, COMMITTEE_CHOICES 

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, help_text="Password must contain at least 8 characters.")
    
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    committee = forms.ChoiceField(choices=COMMITTEE_CHOICES, required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    university_year = forms.CharField(max_length=50, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'committee', 'phone_number', 'university_year', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"] 
        user.set_password(password) 
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    committee = forms.ChoiceField(choices=COMMITTEE_CHOICES, required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    university_year = forms.CharField(max_length=50, required=False)
    
    class Meta:
        model = User
        fields = '__all__'