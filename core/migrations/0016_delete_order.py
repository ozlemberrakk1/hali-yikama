# Generated by Django 5.2 on 2025-04-25 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_carpet_carpet_type_alter_carpet_customer_email_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
