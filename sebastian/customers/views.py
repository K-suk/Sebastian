from django.views import generic
from .models import Customer

class CustomerListView(generic.ListView):
    model = Customer