from django.core.mail import send_mail
from django.template.loader import render_to_string

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
