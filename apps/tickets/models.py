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
    employee = models.ForeignKey('core.Employee', on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return self.subject

