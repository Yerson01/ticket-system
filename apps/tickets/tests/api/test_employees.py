from django.urls import reverse

from rest_framework import status

from apps.core.tests.testcases import LoggedInAPITestCase

from apps.tickets.factories import EmployeeFactory
from apps.tickets.models import Employee
from apps.tickets.serializers import EmployeeSerializer


class TestEmployeeList(LoggedInAPITestCase):
    factory_class = EmployeeFactory
    user_factory_class = factory_class
    manage_url = reverse('tickets:manage-employees')

    def test_create_new_employee_is_success(self):
        payload = self.factory_class.build_dict()
        payload['password'], payload['confirm_password'] = ['test-password'] * 2
        res = self.client.post(self.manage_url, data=payload)
        assert res.status_code == status.HTTP_201_CREATED
        assert 'id' in res.data
        matches = Employee.objects.filter(pk=res.data['id'])
        assert matches.exists()

    def test_invalid_password_confirmation_bad_request(self):
        payload = self.factory_class.build_dict()
        payload['password'] = 'test-password'
        payload['confirm_password'] = 'not-equal'
        res = self.client.post(self.manage_url, data=payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_create_employee_unauthorized(self):
        self.client.logout()
        res = self.client.post(self.manage_url, {})
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_employees_is_successful(self):
        employee1 = self.factory_class.create()
        employee2 = self.factory_class.create()
        res = self.client.get(self.manage_url)
        assert res.status_code == status.HTTP_200_OK
        assert 'count' in res.data and 'results' in res.data
        assert res.data['count'] == 3

        serializer = EmployeeSerializer([self.user, employee1, employee2], many=True)
        assert serializer.data == res.data['results']
