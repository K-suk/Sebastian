from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from accounts.models import User
from customers.models import Customer
from salary_reports.models import SalaryReport
from .models import Job
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
import datetime

class JobListView(generic.ListView):
    model = Job

@login_required
def assign_job_view(request):
    ready_workers = list(User.objects.filter(ready=True))
    customers = list(Customer.objects.filter(task_assigned=False))
    cnt = 0
    for worker in ready_workers:
        for slot in range(worker.shift_count):
            if cnt < len(customers):
                worker.shift_assigned_done = 0
                worker.shift_assigned += 1
                worker.save()
                job = Job(worker=worker, customer=customers[cnt], status='NEW')
                job.save()
                customers[cnt].task_assigned = True
                customers[cnt].save()
                cnt += 1
            else:
                break
    return redirect('jobs:job_list')

@login_required
def receive_contents_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.status = 'IN_PROGRESS'
    job.save()
    return redirect('jobs:job_list')

@login_required
def update_job_link_view(request, job_id):
    if request.method == "POST":
        job = get_object_or_404(Job, id=job_id)
        link = request.POST.get("link")
        if link:
            job.link = link
            job.status = "EVALUATION"
            job.save()
            return redirect('jobs:job_list')
        else:
            return HttpResponseBadRequest("Link is required.")
    return HttpResponseBadRequest("Invalid request method.")

@login_required
def approve_contents_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.status = 'APPROVED'
    job.save()
    return redirect('jobs:job_list')

@login_required
def complete_contents_view(request, job_id):
    today = datetime.date.today()
    job = get_object_or_404(Job, id=job_id)
    user = User.objects.get(id=request.user.id)
    user.worker_credit += 5
    user.shift_assigned -= 1
    user.shift_assigned_done += 1
    user.save()
    salary_report, created = SalaryReport.objects.get_or_create(
        worker=request.user,
        year=today.year,
        month=today.month,
        defaults={'salary': 0, 'penalty': 0, 'job_amount': 0}
    )
    salary_report.salary += 6000
    salary_report.job_amount += 1
    salary_report.save()
    job.status = 'COMPLETED'
    job.save()
    return redirect('jobs:job_list')

@login_required
def improve_contents_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.status = 'IMPROVEMENT'
    job.save()
    return redirect('jobs:job_list')