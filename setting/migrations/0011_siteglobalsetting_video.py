# Generated by Django 4.2 on 2024-05-18 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0010_remove_socialmediasetting_icon_background_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteglobalsetting',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='site/', verbose_name='فیلم معرفی'),
        ),
    ]
