import pytest
from django.urls import reverse

from rest_framework import status

from apps.core.tests.testcases import LoggedInAPITestCase

from apps.tickets.models import Ticket, TicketTimeEntry
from apps.tickets.serializers import TicketTimeEntrySerializer
from apps.tickets.factories import (
    EmployeeFactory,
    TicketTimeEntryFactory,
    TicketFactory
)


class TestTimeEntryList(LoggedInAPITestCase):
    user_factory_class = EmployeeFactory
    factory_class = TicketTimeEntryFactory

    def setUp(self):
        super(TestTimeEntryList, self).setUp()
        self.ticket: Ticket = TicketFactory.create()

    @staticmethod
    def list_url(ticket_id):
        return reverse('tickets:ticket-time-entry-list', args=[ticket_id])

    def test_list_ticket_time_entries_is_success(self):
        time_entry1 = self.factory_class.create(ticket=self.ticket)
        time_entry2 = self.factory_class.create(ticket=self.ticket)
        res = self.client.get(self.list_url(self.ticket.id))
        assert res.status_code == status.HTTP_200_OK
        assert 'count' in res.data and 'results' in res.data
        assert res.data['count'] == 2

        serializer = TicketTimeEntrySerializer([time_entry1, time_entry2], many=True)
        assert serializer.data == res.data['results']

    def test_time_entry_list_unauthorized_response(self):
        self.client.logout()
        time_entry = self.factory_class()
        url = self.list_url(time_entry.ticket.id)
        res = self.client.get(url)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_time_entry_is_successful(self):
        payload = self.factory_class.build_dict()
        url = self.list_url(self.ticket.id)
        res = self.client.post(url, data=payload)
        assert res.status_code == status.HTTP_201_CREATED
        assert 'id' in res.data
        matches = TicketTimeEntry.objects.filter(id=res.data.get('id'))
        assert matches.exists()

    def test_employee_time_entries_by_ticket(self):
        """
        Test that an employee cannot have more than one
        entry by ticket
        """
        my_time_entry = self.factory_class(
            ticket=self.ticket,
            employee=self.user
        )
        payload = self.factory_class.build_dict()
        url = self.list_url(self.ticket.id)
        res = self.client.post(url, data=payload)
        assert res.status_code == status.HTTP_409_CONFLICT


class TestTimeEntryDetail(LoggedInAPITestCase):
    user_factory_class = EmployeeFactory
    factory_class = TicketTimeEntryFactory

    def setUp(self):
        super(TestTimeEntryDetail, self).setUp()
        self.time_entry: TicketTimeEntry = self.factory_class.create(
            employee=self.user
        )

    @staticmethod
    def detail_url(time_entry_id):
        return reverse('tickets:ticket-time-entry-detail', args=(time_entry_id,))

    @staticmethod
    def get_time_entry(entry_id):
        return TicketTimeEntry.objects.get(pk=entry_id)

    def test_edit_time_entry_is_successful(self):
        payload = self.factory_class.build_dict()
        url = self.detail_url(self.time_entry.id)
        res = self.client.put(url, data=payload)

        self.time_entry.refresh_from_db()
        assert res.status_code == status.HTTP_200_OK
        assert self.time_entry.note == payload.get('note')

    def test_partial_edit(self):
        payload = dict(note='I tried to fix...')
        url = self.detail_url( self.time_entry.id)
        res = self.client.patch(url, data=payload)
        assert res.status_code == status.HTTP_200_OK

    def test_cannot_modify_employee_and_ticket_through_the_body(self):
        payload = dict(employee=5, ticket=88932)
        actual_ticket_id = self.time_entry.ticket.id
        url = self.detail_url(self.time_entry.id)
        res = self.client.put(url, data=payload)
        self.time_entry.refresh_from_db()

        assert res.status_code == status.HTTP_200_OK
        assert self.time_entry.employee == self.user
        assert self.time_entry.ticket.id == actual_ticket_id

    def test_only_owner_can_edit_time_entry(self):
        self.client.logout()
        evan = EmployeeFactory(first_name='Evan')
        self.client.force_authenticate(evan)
        entry = self.time_entry
        url = self.detail_url(entry.id)
        res = self.client.put(url, data={})
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_time_entry_is_successful(self):
        time_entry_id = self.time_entry.id
        url = self.detail_url(time_entry_id)
        res = self.client.delete(url)
        assert res.status_code == status.HTTP_204_NO_CONTENT

        with pytest.raises(self.time_entry.DoesNotExist):
            self.get_time_entry(time_entry_id)

    def test_employee_cannot_delete_someone_else_time_entry(self):
        self.client.logout()
        john = EmployeeFactory()
        self.client.force_authenticate(john)
        url = self.detail_url(self.time_entry.id)
        res = self.client.delete(url)
        assert res.status_code == status.HTTP_403_FORBIDDEN
