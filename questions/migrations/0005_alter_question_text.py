# Generated by Django 3.2.4 on 2021-06-23 13:51

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_alter_question_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text',
            field=django_quill.fields.QuillField(),
        ),
    ]
