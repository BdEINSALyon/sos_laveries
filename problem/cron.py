from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from sos_laveries import settings
from .models import Ticket


def notify_pending():
    ticket = Ticket.objects.filter(state=0).count()
    if ticket > 0:
        email = []
        if settings.EMAIL_RESP_LAVERIE != "" and settings.EMAIL_RESP_LAVERIE is not None:
            email.append(settings.EMAIL_RESP_LAVERIE)
        if settings.EMAIL_RESP_SERVICES != "" and settings.EMAIL_RESP_SERVICES is not None:
            email.append(settings.EMAIL_RESP_SERVICES)
        msg_plain = render_to_string('problem/email_pending.txt', {'ticket': ticket, 'site': settings.ALLOWED_HOSTS[0]})
        send_mail(
            '[Laveries] Ticket en attente',
            msg_plain,
            settings.DEFAULT_FROM_EMAIL,
            email,
        )


def old_ticket():
    semaine_3 = timezone.now() - timezone.timedelta(weeks=3)
    semaine_4 = timezone.now() - timezone.timedelta(weeks=4)
    ticket_email = Ticket.objects.filter(state=1).filter(email_reminder_sent=False).filter(date_treatment__lt=semaine_3)
    for ticket in ticket_email:
        date_expire = ticket.date_treatment + timezone.timedelta(weeks=4) - timezone.timedelta(days=1)
        msg_plain = render_to_string('problem/email_reminder_approved.txt',
                                     {'ticket': ticket, 'date_expire': date_expire.date()})
        send_mail(
            'Jetons en attente de récupération',
            msg_plain,
            settings.DEFAULT_FROM_EMAIL,
            [ticket.insa_email],
        )
        ticket.email_reminder_sent = True
        ticket.save()
    ticket_expire = Ticket.objects.filter(state=1).filter(email_reminder_sent=True).filter(date_treatment__lt=semaine_4)
    for ticket in ticket_expire:
        ticket.state = 4
        ticket.save()
