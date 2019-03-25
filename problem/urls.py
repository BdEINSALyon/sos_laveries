from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import DetailView

from . import views
from .models import Ticket

urlpatterns = [
    path('', views.home, name='home_submit'),
    path('submit/<int:building_id>', views.Step2Create, name='step2_submit'),
    path('manager/accept/<int:pk_ticket>', login_required(views.AcceptTicket), name='accept_ticket'),
    path('manager/reject/<int:pk_ticket>', login_required(views.RejectTicket), name='reject_ticket'),
    path('manager/refund/<int:pk_ticket>', login_required(views.ValidRefund), name='valid_refund'),
    path('manager/new', login_required(views.BrowseNew.as_view()), name='to_treat_list'),
    path('manager/all', login_required(views.BrowseAll.as_view()), name='all_list'),
    path('manager', login_required(views.BrowseToRefund.as_view()), name='to_refund_list'),
    path('manager/show/<int:pk>', login_required(DetailView.as_view(model=Ticket)), name='show_ticket'),
]