import factory
from factory.django import DjangoModelFactory

from apps.tickets.models import Employee


class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = 'tickets.Employee'

    username = factory.Faker('word')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')

    @classmethod
    def build_dict(cls, **extra_fields):
        data = factory.build(dict, FACTORY_CLASS=cls, **extra_fields)
        return data
