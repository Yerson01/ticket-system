from rest_framework import serializers

from apps.tickets.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'is_active',
        )
