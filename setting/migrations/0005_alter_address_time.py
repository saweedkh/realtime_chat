# Generated by Django 5.0.2 on 2024-02-15 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0004_address_phone_address_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='time',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ساعات کاری'),
        ),
    ]