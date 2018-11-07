from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home_submit'),
    path('submit/<int:building_id>', views.Step2Create, name='step2_submit'),
]