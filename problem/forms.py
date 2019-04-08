from captcha.fields import ReCaptchaField
from django import forms

from .models import Ticket, Building, Machine


class TicketForm(forms.ModelForm):
    captcha = ReCaptchaField(label="Êtes-vous un robot ? (Are you a bot ?)")

    class Meta:
        model = Ticket
        fields = (
            'machine', 'problem_type', 'number_token_lost', 'user_comment', 'insa_email', 'last_name', 'first_name',
            'room',
            'phone_number',)
        labels = {'machine': "Machine (Machine)", "problem_type": "Type de problème (Problem type)",
                  "number_token_lost": "Nombre de jetons perdus (Number of token lost)",
                  "user_comment": "Commentaires (Comments)", "insa_email": "Adresse Email INSA (INSA Email Address)",
                  "first_name": "Prénom (Firstname)", "last_name": "Nom (Lastname)",
                  "room": "Chambre INSA (Room Number)", "phone_number": "Numéro de téléphone (Phone Number)"}
        widgets = {'user_comment': forms.TextInput}

    def __init__(self, building_id, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        building = Building.objects.filter(pk=building_id)
        self.fields['machine'].queryset = Machine.objects.filter(building__in=building).filter(active=True).order_by(
            "number")


class AcceptForm(forms.Form):
    number_token_refund = forms.IntegerField(required=True, label="Nombre de jetons à rendre",
                                             help_text="Maximum 3 normalement")
    staff_comment = forms.CharField(required=False, label="Commentaire pour le client",
                                    help_text="Optionnel, ajouté dans l'email envoyé au client")
    staff_comment_perm = forms.CharField(required=False, label="Commentaire pour le permanencier BdE",
                                    help_text="Optionnel")


class RejectForm(forms.Form):
    staff_comment = forms.CharField(required=True, label="Commentaire pour le client",
                                    help_text="Obligatoire, ajouté dans l'email après le texte de refus")
    staff_comment_perm = forms.CharField(required=False, label="Commentaire pour le permanencier BdE",
                                         help_text="Optionnel")