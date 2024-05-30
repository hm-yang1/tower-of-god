# Generated by Django 5.0.6 on 2024-05-29 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_delete_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Earbuds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('brand', models.CharField(blank=True, max_length=255)),
                ('img', models.ImageField(upload_to='products/')),
                ('MSRP', models.FloatField(blank=True)),
                ('release_date', models.DateField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('score', models.IntegerField(blank=True)),
                ('pros', models.JSONField(blank=True, default=list)),
                ('cons', models.JSONField(blank=True, default=list)),
                ('reviews', models.JSONField(blank=True, default=list)),
                ('wireless', models.BooleanField()),
                ('battery_life', models.FloatField(blank=True, null=True)),
                ('active_noise_cancellation', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
