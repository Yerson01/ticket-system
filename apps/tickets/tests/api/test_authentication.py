from faker import Faker

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_jwt.serializers import check_payload

from apps.tickets.factories import EmployeeFactory


class TestLogin(APITestCase):
    faker = Faker()
    login_url = reverse('tickets:login')

    def setUp(self):
        self.employee = EmployeeFactory()
        self.password = self.faker.word()
        self.employee.set_password(self.password)
        self.employee.save()

    def test_obtain_jwt_token_with_valid_credentials(self):
        payload = dict(
            username=self.employee.username,
            password=self.password
        )
        res = self.client.post(self.login_url, data=payload)
        assert res.status_code == status.HTTP_201_CREATED
        assert 'token' in res.data
        assert check_payload(res.data['token'])

    def test_use_invalid_credentials_return_400_bad_request(self):
        payload = dict(username=self.employee.username, password='invalid-pass')
        res = self.client.post(self.login_url, data=payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_both_username_and_password_are_required(self):
        res = self.client.post(self.login_url)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        required_fields = ['username', 'password']

        for field in required_fields:
            assert field in res.data
            errors = res.data[field]
            assert errors[0].code == 'required'
