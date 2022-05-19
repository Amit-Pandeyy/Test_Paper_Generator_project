# Generated by Django 3.2.4 on 2021-06-18 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='chapters')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('text', models.TextField()),
                ('hardness', models.CharField(choices=[('basic', 'basic'), ('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='questions')),
                ('marks', models.IntegerField(default=0)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Question', to='questions.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='standard')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='subjects')),
                ('standard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject', to='questions.standard')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='topic')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapter', to='questions.chapter')),
                ('standard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='standard', to='questions.standard')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject', to='questions.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='questions.question')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='standard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Question', to='questions.standard'),
        ),
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Question', to='questions.subject'),
        ),
        migrations.AddField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Question', to='questions.topic'),
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=500)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Option', to='questions.question')),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='standard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapter', to='questions.standard'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapter', to='questions.subject'),
        ),
    ]