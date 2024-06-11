from django.urls import path
from . import views

app_name = 'salary_reports'

urlpatterns = [
    path('report_list', views.SalaryListView.as_view(), name='report_list'),
]