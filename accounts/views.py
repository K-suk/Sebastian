import datetime
import json
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth.views import (LoginView as BaseLoginView, LogoutView as BaseLogoutView,
                                    PasswordChangeDoneView, PasswordChangeView, 
                                    PasswordResetView, PasswordResetDoneView, 
                                    PasswordResetConfirmView, PasswordResetCompleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from jobs.models import Job
from salary_reports.models import SalaryReport
from .forms import LoginForm, ProfileForm
from .models import User

class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            user_data = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            return render(request, 'error.html', {'error': 'User does not exist'})

        today = datetime.date.today()
        salary_report, created = SalaryReport.objects.get_or_create(
            worker=request.user,
            year=today.year,
            month=today.month,
            defaults={'salary': 0, 'penalty': 0, 'job_amount': 0}
        )
        yearly_salary_report = list(SalaryReport.objects.filter(
            worker=request.user,
            year=today.year,
        ).values('month', 'salary'))  # month と salary フィールドを取得
        shifts_info = {
            'shift_assigned': user_data.shift_assigned,
            'shift_assigned_done': user_data.shift_assigned_done
        }
        return render(request, 'index.html', {
            'user_data': user_data,
            'salary_report': salary_report,
            'yearly_salary_report': json.dumps(yearly_salary_report),
            'shifts_info': json.dumps(shifts_info)
        })

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

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            user_data = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            return render(request, 'error.html', {'error': 'User does not exist'})

        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
        })

class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            user_data = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            return render(request, 'error.html', {'error': 'User does not exist'})

        form = ProfileForm(
            initial={
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'tel': user_data.tel,
                'contact_address': user_data.contact_address,
                'shift_count': user_data.shift_count
            }
        )
        return render(request, 'accounts/profile_edit.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        try:
            user_data = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            return render(request, 'error.html', {'error': 'User does not exist'})

        form = ProfileForm(request.POST)
        if form.is_valid():
            user_data.first_name = form.cleaned_data['first_name']
            user_data.last_name = form.cleaned_data['last_name']
            user_data.tel = form.cleaned_data['tel']
            user_data.contact_address = form.cleaned_data['contact_address']
            user_data.shift_count = form.cleaned_data['shift_count']
            user_data.save()  # ここでユーザー情報を保存する
            return redirect('accounts:profile')
        return render(request, 'accounts/profile_edit.html', {
            'form': form
        })

class UserListView(LoginRequiredMixin, generic.ListView):
    model = User

@login_required
def make_ready_view(request):
    if request.user.ready:
        request.user.ready = False
    else:
        new_jobs = list(Job.objects.filter(status='NEW', worker=request.user))
        progress_jobs = list(Job.objects.filter(status='IN_PROGRESS', worker=request.user))
        if (len(new_jobs) == 0 and len(progress_jobs) == 0):
            request.user.ready = True
        else:
            messages.warning(request, 'You have ongoing jobs and cannot mark yourself as ready.')
    request.user.save()
    return redirect('accounts:profile')