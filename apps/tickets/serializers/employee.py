from rest_framework import serializers

from apps.tickets.models import Employee


class ManageEmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Employee
        fields = (
            'id', 'first_name',  'last_name', 'username', 'email',
            'is_active', 'password', 'confirm_password',
        )

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password', '')

        if password != confirm_password:
            raise serializers.ValidationError(
                detail=dict(confirm_password='Passwords does not match'),
                code='invalid_password',
            )

        return attrs


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'is_active',
        )
