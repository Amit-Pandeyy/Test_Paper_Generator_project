# Generated by Django 3.2.5 on 2021-10-22 17:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0024_auto_20211022_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2021, 10, 22, 23, 6, 33, 892371)),
        ),
        migrations.AlterField(
            model_name='question',
            name='updated_at',
            field=models.DateField(default=datetime.datetime(2021, 10, 22, 23, 6, 33, 892423)),
        ),
    ]
