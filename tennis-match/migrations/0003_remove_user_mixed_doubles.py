# Generated by Django 3.1.1 on 2020-12-03 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis-match', '0002_auto_20201202_0303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='mixed_doubles',
        ),
    ]
