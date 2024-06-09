from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from salary_reports.models import SalaryReport

# Create your views here.
class SalaryListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        report_list = SalaryReport.objects.filter(worker=request.user)
        return render(request, 'reports/report_list.html', {
            'report_list': report_list,
        })
