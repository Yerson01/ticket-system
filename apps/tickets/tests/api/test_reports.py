from datetime import timedelta

from django.utils import timezone
from django.urls import reverse
from rest_framework import status

from apps.core.tests.testcases import LoggedInAPITestCase

from apps.tickets.models import Ticket, TicketTimeEntry
from apps.tickets.factories import (
    EmployeeFactory,
    TicketFactory,
    TicketTimeEntryFactory,
)


class TestTicketReport(LoggedInAPITestCase):
    user_factory_class = EmployeeFactory
    list_url = reverse('tickets:report-list')

    def setUp(self):
        super(TestTicketReport, self).setUp()
        self.ticket: Ticket = TicketFactory.create(status=Ticket.Status.CLOSED)
        self.time_start = timezone.now() - timedelta(days=1, minutes=70)
        self.time_end = timezone.now()
        self.time_entry: TicketTimeEntry = TicketTimeEntryFactory.create(
            ticket=self.ticket,
            date_from=self.time_start,
            date_to=self.time_end
        )

    def test_generate_report_with_ticket_total_hours(self):
        res = self.client.get(self.list_url)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 1
        first_result = res.data[0]
        total_seconds = (self.time_end - self.time_start).total_seconds()
        expected_hours = round(total_seconds / 3600, 1)
        assert first_result.get('hours') == expected_hours
