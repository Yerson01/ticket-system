from rest_framework.test import APITestCase


class LoggedInAPITestCase(APITestCase):
    user_factory_class = None

    def setUp(self):
        assert self.user_factory_class is not None
        self.user = self.user_factory_class()
        self.client.force_authenticate(self.user)