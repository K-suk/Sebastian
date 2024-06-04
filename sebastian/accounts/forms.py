from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # 追加
from django import forms
from .models import User

class LoginForm(AuthenticationForm):
    class Meta:
        model = User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'tel', 'contact_address', 'shift_count']