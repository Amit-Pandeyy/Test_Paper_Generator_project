# Generated by Django 3.2.4 on 2021-06-26 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionPaper', '0003_paper_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='marks',
            field=models.IntegerField(default=0),
        ),
    ]