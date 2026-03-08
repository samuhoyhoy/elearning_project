from django import forms  # Django forms
from django.contrib.auth.forms import UserCreationForm  # built-in signup form
from django.contrib.auth.models import User  # auth user model
from .models import UserProfile  # profile model

# signup form that extends UserCreationForm with extra fields
class SignUpForm(UserCreationForm):
    real_name = forms.CharField(max_length=100)  # full name
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)  # student/teacher

    class Meta:
        model = User
        fields = ('username', 'real_name', 'role', 'password1', 'password2')

# simple search form for filtering users
class UserSearchForm(forms.Form):
    query = forms.CharField(label="Search", max_length=100, required=False)
    role = forms.ChoiceField(
        choices=[('', 'All'), ('student', 'Student'), ('teacher', 'Teacher')],
        required=False
    )
