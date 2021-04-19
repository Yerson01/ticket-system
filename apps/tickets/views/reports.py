from django.db.models import F
from django.db.models.functions import ExtractHour

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.tickets.models import Ticket, TicketTimeEntry
from apps.tickets.serializers import TicketReportSerializer


class TicketReportView(ListAPIView):
    queryset = TicketTimeEntry.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TicketReportSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = super(TicketReportView, self).get_queryset()
        queryset = queryset.filter(
            ticket__status=Ticket.Status.CLOSED,
            date_from__isnull=False,
            date_to__isnull=False,
        )
        return queryset


ticket_report_list = TicketReportView.as_view()
