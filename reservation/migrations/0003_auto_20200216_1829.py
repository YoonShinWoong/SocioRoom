# Generated by Django 3.0 on 2020-02-16 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_auto_20200216_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='room_finish_time',
            field=models.TimeField(max_length=10),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='room_start_time',
            field=models.TimeField(max_length=10),
        ),
    ]
