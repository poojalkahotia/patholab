# Generated by Django 5.1.1 on 2025-02-20 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathoapp', '0032_microalbumin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='haematology',
            name='test_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
