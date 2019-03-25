from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView

from sos_laveries import settings
from .forms import HomeForm, TicketForm, AcceptForm, RejectForm
from .models import Ticket, Building


def home(request):
    form = HomeForm(request.POST or None)
    if form.is_valid():
        building = form.cleaned_data['building']
        return redirect(reverse('step2_submit', args=(building.pk,)))
    else:
        return render(request, 'problem/home_form.html', {"form": form})


def Step2Create(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    if request.method == 'POST':
        form = TicketForm(building_id, request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.state = 0
            ticket.save()
            if ticket.problem_type in {0, 2, 3}:
                email = []
                if ticket.machine.building.email_resp != "" and ticket.machine.building.email_resp is not None:
                    email.append(ticket.machine.building.email_resp)
                if settings.EMAIL_RESP_LAVERIE != "" and settings.EMAIL_RESP_LAVERIE is not None:
                    email.append(settings.EMAIL_RESP_LAVERIE)
                if settings.EMAIL_RESP_SERVICES != "" and settings.EMAIL_RESP_SERVICES is not None:
                    email.append(settings.EMAIL_RESP_SERVICES)
                msg_plain = render_to_string('problem/email_urgent.txt', {'ticket': ticket})
                send_mail(
                    '[Laveries] Problème urgent Bât ' + ticket.machine.building.name,
                    msg_plain,
                    settings.DEFAULT_FROM_EMAIL,
                    email,
                )
            return redirect('home_submit')
        else:
            return render(request, 'problem/step2_form.html', {'form': form, "building": building})
    else:
        form = TicketForm(building_id)
    return render(request, 'problem/step2_form.html', {'form': form, "building": building})



class BrowseNew(ListView):
    paginate_by = 25
    model=Ticket
    def get_queryset(self):
        return Ticket.objects.filter(state=0).order_by('-date_submission')


class BrowseAll(ListView):
    paginate_by = 25
    model = Ticket
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
    ticket = Ticket.objects.get(pk=pk_ticket)
    if(ticket.number_token_lost>3):
        number_ticket_refund=3
    else:
        number_ticket_refund=ticket.number_token_lost
    form = AcceptForm(request.POST or None, initial={"number_token_refund": number_ticket_refund})
    if form.is_valid():
        ticket.date_treatment=timezone.now()
        ticket.number_token_refund=form.cleaned_data["number_token_refund"]
        ticket.state=1
        ticket.staff_comment=form.cleaned_data["staff_comment"]
        ticket.save()
        msg_plain = render_to_string('problem/email_approved.txt', {'ticket': ticket})
        send_mail(
            'Validation de la demande de remboursement',
            msg_plain,
            settings.DEFAULT_FROM_EMAIL,
            [ticket.insa_email],
        )
        return redirect(reverse("to_treat_list"))
    return render(request, 'problem/form_admin.html', {"object": ticket, "form": form, "action": "accept"})


def RejectTicket(request, pk_ticket):
    form = RejectForm(request.POST or None)
    ticket = Ticket.objects.get(pk=pk_ticket)
    if form.is_valid():
        ticket.date_treatment=timezone.now()
        ticket.number_token_refund=0
        ticket.state=2
        ticket.staff_comment=form.cleaned_data["staff_comment"]
        ticket.save()
        msg_plain = render_to_string('problem/email_rejected.txt', {'ticket': ticket})
        send_mail(
            'Rejet de la demande de remboursement',
            msg_plain,
            settings.DEFAULT_FROM_EMAIL,
            [ticket.insa_email],
        )
        return redirect(reverse("to_treat_list"))
    return render(request, 'problem/form_admin.html', {"object": ticket, "form": form, "action": "reject"})
