# Generated by Django 3.1.7 on 2021-04-17 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_auto_20210417_1941'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='tickettimeentry',
            constraint=models.UniqueConstraint(fields=('ticket', 'employee'), name='ticket_employee'),
        ),
    ]
