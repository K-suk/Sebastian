from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import (LoginView as BaseLoginView, LogoutView as BaseLogoutView,
                                    PasswordChangeDoneView, PasswordChangeView, 
                                    PasswordResetView, PasswordResetDoneView, 
                                    PasswordResetConfirmView, PasswordResetCompleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import LoginForm

class IndexView(TemplateView):
    """ ホームビュー """
    template_name = "index.html"
    
# ログインビューを作成
class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    
class LogoutView(BaseLogoutView):
    success_url = reverse_lazy("accounts:index")
    
class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'accounts/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context

class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    """パスワード変更完了"""
    template_name = 'accounts/password_change_done.html'
    
class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'accounts/mail_template/reset/subject.txt'
    email_template_name = 'accounts/mail_template/reset/message.txt'
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'accounts/password_reset_complete.html'