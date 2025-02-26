# Generated by Django 5.1.1 on 2024-10-04 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathoapp', '0008_alter_urinetest_normal_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='urinetest',
            name='patient_age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='urinetest',
            name='patient_email',
            field=models.EmailField(default='noemail@example.com', max_length=254),
        ),
        migrations.AddField(
            model_name='urinetest',
            name='patient_gender',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='urinetest',
            name='patient_mobile',
            field=models.CharField(default='Unknown', max_length=15),
        ),
        migrations.AddField(
            model_name='urinetest',
            name='patient_name',
            field=models.CharField(default='Unknown Patient', max_length=255),
        ),
        migrations.AlterField(
            model_name='urinetest',
            name='other_test',
            field=models.CharField(max_length=50),
        ),
    ]
