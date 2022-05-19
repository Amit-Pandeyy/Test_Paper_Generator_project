# Generated by Django 3.2.5 on 2021-10-02 18:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0004_alter_coupon_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='user',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]