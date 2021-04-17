import factory
from factory.django import DjangoModelFactory


class TicketTimeEntryFactory(DjangoModelFactory):
    class Meta:
        model = 'tickets.TicketTimeEntry'

    ticket = factory.SubFactory('apps.tickets.factories.TicketFactory')
    employee = factory.SubFactory('apps.tickets.factories.EmployeeFactory')
    note = factory.Faker('sentence', nb_words=8)
    date_from = factory.Faker('date_time')
    date_to = factory.Faker('date_time')

    @classmethod
    def build_dict(cls, **extra_fields):
        data = factory.build(dict, FACTORY_CLASS=cls)
        data.pop('employee', None)
        data.pop('ticket', None)
        data.update(**extra_fields)
        return data


