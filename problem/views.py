from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import HomeForm, TicketForm
from django.views.generic import ListView, DetailView
import sys


def home(request):
    form = HomeForm(request.POST or None)
    if form.is_valid():
        building = form.cleaned_data['building']
        return redirect(reverse('step2_submit', args=(building.pk,)))
    else:
        return render(request, 'problem/home_form.html', locals())


def Step2Create(request, building_id):
    if request.method == 'POST':
        form = TicketForm(building_id, request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.state = 0
            ticket.save()
            return redirect('home_submit')
        else:
            return render(request, 'problem/step2_form.html', {'form': form})
    else:
        form = TicketForm(building_id)
    return render(request, 'problem/step2_form.html', {'form': form})
