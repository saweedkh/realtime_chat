# Generated by Django 5.0.2 on 2024-02-16 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0006_address_map_address_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteglobalsetting',
            name='map',
        ),
        migrations.AlterField(
            model_name='address',
            name='map',
            field=models.TextField(blank=True, help_text='کد html نقشه را وارد کنید', null=True, verbose_name='نقشه'),
        ),
    ]