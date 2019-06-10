from import_export import resources
from .models import Ticket
from import_export.fields import Field


class TicketResource(resources.ModelResource):
    get_problem = Field(attribute='get_problem')
    get_state = Field(attribute='get_state')
    count_same_email = Field(attribute='count_same_email')

    class Meta:
        model = Ticket
        fields = ('id', 'machine__building__name', 'machine__number', 'number_token_lost', 'staff_user__username', 'number_token_refund', 'date_submission', 'date_treatment', 'date_refund')
        export_order = ('id', 'count_same_email', 'machine__building__name', 'machine__number', 'get_problem', 'number_token_lost', 'staff_user__username', 'number_token_refund', 'get_state', 'date_submission', 'date_treatment', 'date_refund')
