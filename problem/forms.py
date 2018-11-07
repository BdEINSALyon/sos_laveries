from django import forms
from .models import Ticket, Building, Machine

class HomeForm(forms.Form):
    building = forms.ModelChoiceField(queryset=Building.objects.filter(active=True))

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields=('machine','problem_type','number_token_lost','user_comment','insa_email','last_name','first_name','room','phone_number',)
    def __init__(self, building_id, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        building = Building.objects.filter(pk=building_id)
        self.fields['machine'].queryset = Machine.objects.filter(building__in=building)

class AcceptForm(forms.Form):
    number_token_refund = forms.IntegerField(required=True)
    staff_comment = forms.CharField(required=False)