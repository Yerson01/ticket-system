from rest_framework import serializers

from apps.core.exceptions import Conflict
from apps.tickets.models import TicketTimeEntry, Employee, Ticket
from apps.tickets.serializers import EmployeeSerializer


class TicketTimeEntrySerializer(serializers.ModelSerializer):
    employee_detail = EmployeeSerializer(source='employee', read_only=True)

    class Meta:
        model = TicketTimeEntry
        fields = '__all__'
        read_only_fields = ('employee', 'ticket',)

    def get_employee_from_context(self):
        employee = self.context.get('employee')
        assert isinstance(employee, Employee), (
            '%s: employee need to be passed in context',
            self.__class__.__name__
        )
        return employee

    def get_ticket_from_context(self):
        ticket = self.context.get('ticket')
        assert isinstance(ticket, Ticket), (
            '%s: ticket need to be passed in context',
            self.__class__.__name__
        )
        return ticket

    def create(self, validated_data):
        ticket = self.get_ticket_from_context()
        employee = self.get_employee_from_context()
        employee_tickets = TicketTimeEntry.objects.filter(
            employee_id=employee.id,
            ticket_id=ticket.id
        )
        if employee_tickets.exists():
            raise Conflict('This employee has already created a ticket')

        validated_data.update(employee=employee, ticket=ticket)
        return super(TicketTimeEntrySerializer, self).create(validated_data)
