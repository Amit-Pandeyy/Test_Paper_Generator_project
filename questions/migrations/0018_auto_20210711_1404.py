# Generated by Django 3.2.5 on 2021-07-11 08:34

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0017_auto_20210711_1401'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='image',
        ),
        migrations.AlterField(
            model_name='solution',
            name='text',
            field=tinymce.models.HTMLField(),
        ),
    ]