from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm # 追加
from django import forms
from .models import User

class LoginForm(AuthenticationForm):
    class Meta:
        model = User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name','tel',
            'contact_address', 'shift_count'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tel': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_address': forms.TextInput(attrs={'class': 'form-control'}),
            'shift_count': forms.NumberInput(attrs={'class': 'form-control'}),
        }