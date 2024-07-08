# Generated by Django 5.0.2 on 2024-02-13 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0002_remove_siteglobalsetting_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteglobalsetting',
            name='about_en',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات فوتر'),
        ),
        migrations.AddField(
            model_name='siteglobalsetting',
            name='about_fa',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات فوتر'),
        ),
        migrations.AlterField(
            model_name='siteglobalsetting',
            name='about',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات فوتر'),
        ),
    ]