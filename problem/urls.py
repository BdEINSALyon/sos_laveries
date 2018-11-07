from django.urls import path, include
from django.views.generic import ListView, DetailView
from . import views
from .models import Ticket

urlpatterns = [
    path('', views.home, name='home_submit'),
    path('submit/<int:building_id>', views.Step2Create, name='step2_submit'),
    path('manager/open',ListView.as_view(model=Ticket,)),
]