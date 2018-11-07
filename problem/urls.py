from django.urls import path, include
from django.views.generic import ListView, DetailView
from . import views
from .models import Ticket

urlpatterns = [
    path('', views.home, name='home_submit'),
    path('submit/<int:building_id>', views.Step2Create, name='step2_submit'),
    path('manager/accept/<int:pk_ticket>', views.AcceptTicket, name='accept_ticket'),
    path('manager/reject/<int:pk_ticket>', views.RejectTicket, name='reject_ticket'),
    path('manager/refund/<int:pk_ticket>', views.ValidRefund, name='valid_refund'),
    path('manager/new',views.BrowseNew.as_view(), name='to_treat_list'),
    path('manager/all',views.BrowseAll.as_view(), name='all_list'),
    path('manager',views.BrowseToRefund.as_view(), name='to_refund_list'),
    path('manager/show/<int:pk>', DetailView.as_view(model=Ticket), name='show_ticket'),
]