# Generated by Django 5.2 on 2025-04-25 16:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_delete_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='carpet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.carpet'),
        ),
    ]
