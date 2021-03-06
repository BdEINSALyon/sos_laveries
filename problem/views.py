from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView
from django.http import HttpResponse


from sos_laveries import settings
from .forms import TicketForm, AcceptForm, RejectForm
from .models import Ticket, Building
from .resources import TicketResource

def home(request):
    building = Building.objects.filter(active=True).order_by("name")
    return render(request, 'problem/home_form.html', {"building": building})


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
            return render(request, 'problem/submit_ok.html', {'ticket': ticket})
        else:
            return render(request, 'problem/step2_form.html', {'form': form, "building": building})
    else:
        form = TicketForm(building_id)
    return render(request, 'problem/step2_form.html', {'form': form, "building": building})


class BrowseNew(ListView):
    paginate_by = 25
    model = Ticket

    def get_queryset(self):
        return Ticket.objects.filter(state=0).order_by('-date_submission')


class BrowseAll(ListView):
    paginate_by = 25
    model = Ticket
    ordering = ['-date_submission']


class BrowseToRefund(ListView):
    model = Ticket
    template_name = 'problem/torefund_list.html'

    def get_queryset(self):
        return Ticket.objects.filter(state=1).order_by('-date_submission')


def ValidRefund(request, pk_ticket):
    ticket = Ticket.objects.get(pk=pk_ticket)
    ticket.state = 3
    ticket.date_refund = timezone.now()
    ticket.save()
    return redirect(reverse('to_refund_list'))


def AcceptTicket(request, pk_ticket):
    ticket = Ticket.objects.get(pk=pk_ticket)
    if (ticket.number_token_lost > 3):
        number_ticket_refund = 3
    else:
        number_ticket_refund = ticket.number_token_lost
    form = AcceptForm(request.POST or None, initial={"number_token_refund": number_ticket_refund})
    if form.is_valid():
        number_token_refund = int(form.cleaned_data["number_token_refund"])
        if number_token_refund > 0:
            ticket.date_treatment = timezone.now()
            ticket.number_token_refund = number_ticket_refund
            ticket.state = 1
            ticket.staff_comment = form.cleaned_data["staff_comment"]
            ticket.staff_comment_perm = form.cleaned_data["staff_comment_perm"]
            ticket.staff_user = request.user
            ticket.save()
            msg_plain = render_to_string('problem/email_approved.txt', {'ticket': ticket})
            send_mail(
                'Validation de la demande de remboursement',
                msg_plain,
                settings.DEFAULT_FROM_EMAIL,
                [ticket.insa_email],
            )
        else:
            ticket.date_treatment = timezone.now()
            ticket.number_token_refund = number_ticket_refund
            ticket.state = 3
            ticket.staff_comment_perm = form.cleaned_data["staff_comment_perm"]
            ticket.staff_user = request.user
            ticket.save()
        return redirect(reverse("to_treat_list"))
    return render(request, 'problem/form_admin.html', {"object": ticket, "form": form, "action": "accept"})


def RejectTicket(request, pk_ticket):
    form = RejectForm(request.POST or None)
    ticket = Ticket.objects.get(pk=pk_ticket)
    if form.is_valid():
        ticket.date_treatment = timezone.now()
        ticket.number_token_refund = 0
        ticket.state = 2
        ticket.staff_comment = form.cleaned_data["staff_comment"]
        ticket.staff_comment_perm = form.cleaned_data["staff_comment_perm"]
        ticket.staff_user = request.user
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


def export_ticket(request):
    ticket_resource = TicketResource()
    dataset = ticket_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="tickets.xls"'
    return response

def stats(request):
    ticket_30j = Ticket.objects.filter(date_submission__gte=timezone.now() - timezone.timedelta(days=30))
    somme30j = ticket_30j.count()
    building_list = Building.objects.all()
    stats_building=[]
    for building in building_list:
        stats_building.append((building.name, ticket_30j.filter(machine__building=building).count()))
    return render(request, 'problem/stats_admin.html', {"stats_building": stats_building, "somme30j": somme30j})