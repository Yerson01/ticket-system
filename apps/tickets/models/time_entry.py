from django.db import models


class TicketTimeEntry(models.Model):
    class Meta:
        default_related_name = 'time_entries'
        constraints = [
            models.UniqueConstraint(fields=['ticket', 'employee'], name='ticket_employee'),
        ]

    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.CASCADE)
    employee = models.ForeignKey('tickets.Employee', on_delete=models.CASCADE)
    note = models.CharField(max_length=255, blank=True, null=True)
    date_from = models.DateTimeField(auto_now_add=True)
    date_to = models.DateTimeField(null=True)

    def __str__(self):
        return '%s Time Entry' % self.ticket.subject
