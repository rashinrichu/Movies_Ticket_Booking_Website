# Generated by Django 3.2.16 on 2023-08-10 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_ticket', '0009_booking_seats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='num_tickets',
        ),
        migrations.AlterField(
            model_name='booking',
            name='seats',
            field=models.ManyToManyField(to='movies_ticket.Seat'),
        ),
    ]
