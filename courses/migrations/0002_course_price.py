# Generated by Django 4.1.7 on 2023-03-12 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.CharField(default='10$', max_length=50),
        ),
    ]
