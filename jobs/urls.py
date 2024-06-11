from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('job_list', views.JobListView.as_view(), name='job_list'),
    path('approve_wait_list', views.ApproveJobListView.as_view(), name='approve_wait_list'),
    path('assign_job/', views.assign_job_view, name='assign_job'),
    path('receive_content/<int:job_id>', views.receive_contents_view, name='receive_content'),
    path('update_job_link/<int:job_id>/', views.update_job_link_view, name='update_job_link'),
    path('approve_content/<int:job_id>/', views.approve_contents_view, name='approve_content'),
    path('complete_content/<int:job_id>/', views.complete_contents_view, name='complete_content'),
    path('improve_content/<int:job_id>/', views.improve_contents_view, name='improve_content'),
]