# Generated by Django 5.0.6 on 2024-06-17 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_laptop_screen_resolution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptop',
            name='processor',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
