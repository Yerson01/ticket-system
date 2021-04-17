import factory
from factory.django import DjangoModelFactory

from apps.tickets.models import Ticket


def add_employees(obj, created, employees):
    is_model_instance = isinstance(obj, Ticket)

    if created and employees and is_model_instance:
        obj.employees.set(employees)


class TicketFactory(DjangoModelFactory):
    class Meta:
        model = 'tickets.Ticket'

    subject = factory.Faker('word')
    description = factory.Faker('text')
    employees = factory.PostGeneration(add_employees)

    @classmethod
    def build_dict(cls, **extra_fields):
        data = factory.build(dict, FACTORY_CLASS=cls, **extra_fields)
        return data
