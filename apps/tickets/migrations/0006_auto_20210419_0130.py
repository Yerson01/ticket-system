# Generated by Django 3.1.7 on 2021-04-19 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_auto_20210417_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickettimeentry',
            name='date_from',
            field=models.DateTimeField(null=True),
        ),
    ]