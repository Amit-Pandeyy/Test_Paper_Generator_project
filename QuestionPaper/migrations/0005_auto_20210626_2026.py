# Generated by Django 3.1.7 on 2021-06-26 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionPaper', '0004_alter_paper_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
