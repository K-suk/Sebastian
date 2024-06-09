from django.views import generic
from .models import Customer
from django.contrib.auth.mixins import LoginRequiredMixin

class CustomerListView(generic.ListView, LoginRequiredMixin):
    model = Customer