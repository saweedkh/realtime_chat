# Generated by Django 4.2 on 2024-07-11 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_alter_link_options_alter_groupmember_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='expired',
            field=models.DateTimeField(blank=True, null=True, verbose_name='تاریخ انقضا'),
        ),
        migrations.AddField(
            model_name='link',
            name='joined_member',
            field=models.PositiveIntegerField(default=0, verbose_name='تعداد کاربران عضو شده'),
        ),
        migrations.AddField(
            model_name='link',
            name='member_limit',
            field=models.PositiveIntegerField(default=0, help_text='مقدار 0 به منظور بدون محدودیت است', verbose_name='محدودیت اعضا'),
        ),
    ]
