# Generated by Django 4.2 on 2024-07-11 05:12

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_link_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='group',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='user', chained_model_field='groupmember', on_delete=django.db.models.deletion.CASCADE, to='chat.group', verbose_name='گروه'),
        ),
    ]