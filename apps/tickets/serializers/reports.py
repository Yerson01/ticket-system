from rest_framework import serializers

from apps.tickets.models import TicketTimeEntry
from apps.tickets.serializers import EmployeeSerializer


class TicketReportSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    date_start = serializers.DateTimeField(source='date_from', read_only=True)
    date_end = serializers.DateTimeField(source='date_to', read_only=True)
    hours = serializers.SerializerMethodField()

    class Meta:
        model = TicketTimeEntry
        fields = (
            'ticket_id', 'note', 'employee', 'date_start',
            'date_end', 'hours',
        )

    def get_hours(self, instance):
        time_diff = instance.date_to - instance.date_from
        total_hours = time_diff.total_seconds() / 3600
        return round(total_hours, 1)



