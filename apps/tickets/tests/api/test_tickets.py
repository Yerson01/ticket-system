import pytest

from django.urls import reverse

from rest_framework import status

from apps.core.tests.testcases import LoggedInAPITestCase

from apps.tickets.models import Ticket
from apps.tickets.factories import EmployeeFactory, TicketFactory
from apps.tickets.serializers import TicketSerializer


class TestTicketList(LoggedInAPITestCase):
    user_factory_class = EmployeeFactory
    factory_class = TicketFactory
    list_url = reverse('tickets:ticket-list')

    def test_create_new_ticket_is_success(self):
        create_kwargs = {'employees': (EmployeeFactory().id,)}
        payload = self.factory_class.build_dict(**create_kwargs)
        res = self.client.post(self.list_url, data=payload)
        assert res.status_code == status.HTTP_201_CREATED
        assert 'id' in res.data
        matches = Ticket.objects.filter(id=res.data.get('id'))
        assert matches.exists()

    def test_cannot_create_ticket_unauthenticated(self):
        self.client.logout()
        res = self.client.post(self.list_url)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_tickets_is_successful(self):
        ticket1 = self.factory_class()
        ticket2 = self.factory_class()
        res = self.client.get(self.list_url)
        assert 'count' in res.data and 'results' in res.data
        assert res.data['count'] == 2

        serializer = TicketSerializer([ticket1, ticket2], many=True)
        assert res.data['results'] == serializer.data


class TestTicketDetail(LoggedInAPITestCase):
    user_factory_class = EmployeeFactory
    factory_class = TicketFactory

    def setUp(self):
        super(TestTicketDetail, self).setUp()
        self.ticket: Ticket = self.factory_class.create()

    @staticmethod
    def get_ticket(ticket_id):
        return Ticket.objects.get(pk=ticket_id)

    @staticmethod
    def detail_url(ticket_id):
        return reverse('tickets:ticket-detail', args=[ticket_id])

    @property
    def payload(self):
        employees = (EmployeeFactory().id,)
        payload = self.factory_class.build_dict(employees=employees)
        return payload

    def retrieve_ticket_detail_is_successful(self):
        res = self.client.get(self.detail_url(self.ticket.id))
        assert res.status_code == status.HTTP_200_OK
        serializer = TicketSerializer(self.ticket)
        assert serializer.data == res.data

    def test_delete_ticket_is_successful(self):
        id_before_delete = self.ticket.id
        url = self.detail_url(self.ticket.id)
        res = self.client.delete(url)
        assert res.status_code == status.HTTP_204_NO_CONTENT

        with pytest.raises(self.ticket.DoesNotExist):
            self.get_ticket(id_before_delete)

    def test_update_a_ticket_is_successful(self):
        payload = self.payload
        url = self.detail_url(self.ticket.id)
        res = self.client.put(url, data=payload)
        assert res.status_code == status.HTTP_200_OK

        self.ticket.refresh_from_db()
        assert self.ticket.subject == payload.get('subject')
        assert self.ticket.description == payload.get('description')

    def test_cannot_update_ticket_unauthorized(self):
        self.client.logout()
        url = self.detail_url(self.ticket.id)
        res = self.client.put(url)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_partial_update(self):
        payload = dict(subject='Mouse not working')
        url = self.detail_url(self.ticket.id)
        res = self.client.patch(url, data=payload)
        self.ticket.refresh_from_db()

        assert res.status_code == status.HTTP_200_OK
        assert self.ticket.subject == payload.get('subject')
