from django.db import models


class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        CLOSED = 'closed', 'Closed'

    class Meta:
        default_related_name = 'tickets'

    subject = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.OPEN)
    employees = models.ManyToManyField('tickets.Employee')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
