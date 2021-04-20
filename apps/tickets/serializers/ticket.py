from rest_framework import serializers

from apps.tickets.models import Ticket
from apps.tickets.serializers import EmployeeSerializer


class TicketSerializer(serializers.ModelSerializer):
    employee_details = EmployeeSerializer(source='employees', read_only=True, many=True)

    class Meta:
        model = Ticket
        fields = '__all__'