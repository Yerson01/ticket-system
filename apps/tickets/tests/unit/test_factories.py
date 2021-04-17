from django.test.testcases import TestCase

from apps.core.tests.mixins import FactoryTestMixin

from apps.tickets.models import Employee, Ticket, TicketTimeEntry
from apps.tickets.factories import (
    EmployeeFactory,
    TicketFactory,
    TicketTimeEntryFactory
)


class TestEmployeeFactory(FactoryTestMixin, TestCase):
    factory_class = EmployeeFactory
    model_class = Employee


class TestTicketFactory(FactoryTestMixin, TestCase):
    factory_class = TicketFactory
    model_class = Ticket


class TestTicketTimeEntryFactory(FactoryTestMixin, TestCase):
    factory_class = TicketTimeEntryFactory
    model_class = TicketTimeEntry
