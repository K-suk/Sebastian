from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from accounts.models import User
from customers.models import Customer
from jobs.models import Job
import datetime

class AssignJobViewTest(TestCase):

    def setUp(self):
        # ユーザーのセットアップ
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            account_id='user1',
            password='password1',
            first_name='First1',
            last_name='Last1',
            tel='111-1111',
            contact_address='Address1',
            shift_count=1,
            worker_credit=10,
            ready=True
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            account_id='user2',
            password='password2',
            first_name='First2',
            last_name='Last2',
            tel='222-2222',
            contact_address='Address2',
            shift_count=1,
            worker_credit=20,
            ready=True
        )
        self.user3 = User.objects.create_user(
            email='user3@example.com',
            account_id='user3',
            password='password3',
            first_name='First3',
            last_name='Last3',
            tel='333-3333',
            contact_address='Address3',
            shift_count=1,
            worker_credit=15,
            ready=True
        )

        # 今日の日付
        today = timezone.now().date()

        # カスタマーのセットアップ
        self.customer1 = Customer.objects.create(
            email='customer1@example.com',
            first_name='Customer1',
            last_name='Test1',
            contact_address='Customer Address1',
            task_completed=False,
            task_assigned=False,
            due=today - datetime.timedelta(days=1)  # 昨日
        )

        # カスタマー2 - 期限日が今日
        self.customer2 = Customer.objects.create(
            email='customer2@example.com',
            first_name='Customer2',
            last_name='Test2',
            contact_address='Customer Address2',
            task_completed=False,
            task_assigned=False,
            due=today  # 今日
        )

        # カスタマー3 - 期限日が今日より後
        self.customer3 = Customer.objects.create(
            email='customer3@example.com',
            first_name='Customer3',
            last_name='Test3',
            contact_address='Customer Address3',
            task_completed=False,
            task_assigned=False,
            due=today + datetime.timedelta(days=1)  # 明日
        )

    def test_list_check(self):
        ready_workers = list(User.objects.filter(ready=True).order_by('-worker_credit'))
        
        # テスト内容
        self.assertEqual(len(ready_workers), 3)
        self.assertEqual(ready_workers[0].account_id, 'user2')
        self.assertEqual(ready_workers[1].account_id, 'user3')
        self.assertEqual(ready_workers[2].account_id, 'user1')
        
    def test_customer_list(self):
        today = timezone.now().date()
        customers = list(Customer.objects.filter(task_assigned=False, due__lte=today))

        # テスト内容
        self.assertEqual(len(customers), 2)  # 期限日が今日以下のカスタマーは2つ
        self.assertIn(self.customer1, customers)
        self.assertIn(self.customer2, customers)
        self.assertNotIn(self.customer3, customers)
        
    def test_assign_job_view_more_shift_count(self):
        self.client.login(account_id='user1', password='password1')
        response = self.client.get(reverse('jobs:assign_job'))
        self.assertEqual(response.status_code, 302)
        
        jobs = Job.objects.all()
        self.assertEqual(len(jobs), 2)
        
        assigned_jobs_user1 = Job.objects.filter(worker=self.user1)
        assigned_jobs_user2 = Job.objects.filter(worker=self.user2)
        assigned_jobs_user3 = Job.objects.filter(worker=self.user3)
        
        self.assertEqual(len(assigned_jobs_user1), 0)
        self.assertEqual(len(assigned_jobs_user2), 1)
        self.assertEqual(len(assigned_jobs_user3), 1)
    
    def test_assign_job_view_same_shift_count(self):
        self.user2.shift_count = 0
        self.user2.save()
        self.client.login(account_id='user1', password='password1')
        response = self.client.get(reverse('jobs:assign_job'))
        self.assertEqual(response.status_code, 302)
        
        jobs = Job.objects.all()
        self.assertEqual(len(jobs), 2)
        
        assigned_jobs_user1 = Job.objects.filter(worker=self.user1)
        assigned_jobs_user2 = Job.objects.filter(worker=self.user2)
        assigned_jobs_user3 = Job.objects.filter(worker=self.user3)
        
        self.assertEqual(len(assigned_jobs_user1), 1)
        self.assertEqual(len(assigned_jobs_user2), 0)
        self.assertEqual(len(assigned_jobs_user3), 1)
    
    def test_assign_job_view_less_shift_count(self):
        self.user2.shift_count = 0
        self.user2.save()
        self.user3.shift_count = 0
        self.user3.save()
        self.client.login(account_id='user1', password='password1')
        response = self.client.get(reverse('jobs:assign_job'))
        self.assertEqual(response.status_code, 302)
        
        jobs = Job.objects.all()
        self.assertEqual(len(jobs), 1)
        
        assigned_jobs_user1 = Job.objects.filter(worker=self.user1)
        assigned_jobs_user2 = Job.objects.filter(worker=self.user2)
        assigned_jobs_user3 = Job.objects.filter(worker=self.user3)
        
        self.assertEqual(len(assigned_jobs_user1), 1)
        self.assertEqual(len(assigned_jobs_user2), 0)
        self.assertEqual(len(assigned_jobs_user3), 0)
        
    def test_assign_job_view_zero_shift_count(self):
        self.user1.shift_count = 0
        self.user1.save()
        self.user2.shift_count = 0
        self.user2.save()
        self.user3.shift_count = 0
        self.user3.save()
        self.client.login(account_id='user1', password='password1')
        response = self.client.get(reverse('jobs:assign_job'))
        self.assertEqual(response.status_code, 302)
        
        jobs = Job.objects.all()
        self.assertEqual(len(jobs), 0)
        
        assigned_jobs_user1 = Job.objects.filter(worker=self.user1)
        assigned_jobs_user2 = Job.objects.filter(worker=self.user2)
        assigned_jobs_user3 = Job.objects.filter(worker=self.user3)
        
        self.assertEqual(len(assigned_jobs_user1), 0)
        self.assertEqual(len(assigned_jobs_user2), 0)
        self.assertEqual(len(assigned_jobs_user3), 0)
        
    def test_assign_job_view_zero_shift_count(self):
        self.customer1.due = timezone.now().date() + datetime.timedelta(days=1)
        self.customer1.save()
        self.customer2.due = timezone.now().date() + datetime.timedelta(days=1)
        self.customer2.save()
        self.client.login(account_id='user1', password='password1')
        response = self.client.get(reverse('jobs:assign_job'))
        self.assertEqual(response.status_code, 302)
        
        jobs = Job.objects.all()
        self.assertEqual(len(jobs), 0)
        
        assigned_jobs_user1 = Job.objects.filter(worker=self.user1)
        assigned_jobs_user2 = Job.objects.filter(worker=self.user2)
        assigned_jobs_user3 = Job.objects.filter(worker=self.user3)
        
        self.assertEqual(len(assigned_jobs_user1), 0)
        self.assertEqual(len(assigned_jobs_user2), 0)
        self.assertEqual(len(assigned_jobs_user3), 0)