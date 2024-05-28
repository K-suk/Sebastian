from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # 追加

from .models import User

class LoginForm(AuthenticationForm):
    class Meta:
        model = User