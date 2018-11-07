from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import HomeForm, TicketForm, AcceptForm
from django.views.generic import ListView, DetailView
from .models import Ticket
from django.utils import timezone


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

class BrowseNew(ListView):
    paginate_by = 25
    model=Ticket
    def get_queryset(self):
        return Ticket.objects.filter(state=0).order_by('-date_submission')

class BrowseAll(ListView):
    paginate_by = 25
    model=Ticket
    ordering = ['-date_submission']

class BrowseToRefund(ListView):
    model=Ticket
    template_name = 'problem/torefund_list.html'
    def get_queryset(self):
        return Ticket.objects.filter(state=1).order_by('-date_submission')

def ValidRefund(request, pk_ticket):
    ticket = Ticket.objects.get(pk=pk_ticket)
    ticket.state=3
    ticket.date_refund=timezone.now()
    ticket.save()
    return redirect(reverse('to_refund_list'))

def AcceptTicket(request, pk_ticket):
    form = AcceptForm(request.POST or None)
    if form.is_valid():
        state = True
    return render(request, 'problem/step2_form.html', locals())
