# Generated by Django 3.2.4 on 2021-06-20 17:31

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text',
            field=tinymce.models.HTMLField(),
        ),
    ]