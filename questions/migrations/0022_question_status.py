# Generated by Django 3.2.5 on 2021-07-24 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0021_alter_option_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='status',
            field=models.CharField(blank=True, default='No', max_length=500, null=True),
        ),
    ]