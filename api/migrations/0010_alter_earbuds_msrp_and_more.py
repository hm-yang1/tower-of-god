# Generated by Django 5.0.6 on 2024-05-29 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_headphones_keyboard_laptop_mouse_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earbuds',
            name='MSRP',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='earbuds',
            name='active_noise_cancellation',
            field=models.BooleanField(blank=True),
        ),
        migrations.AlterField(
            model_name='earbuds',
            name='brand',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='earbuds',
            name='img',
            field=models.ImageField(null=True, upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='earbuds',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='earbuds',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='earbuds',
            name='wireless',
            field=models.BooleanField(blank=True),
        ),
        migrations.AlterField(
            model_name='headphones',
            name='MSRP',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='headphones',
            name='brand',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='headphones',
            name='img',
            field=models.ImageField(null=True, upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='headphones',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='headphones',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='keyboard',
            name='MSRP',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='keyboard',
            name='brand',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='keyboard',
            name='img',
            field=models.ImageField(null=True, upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='keyboard',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='keyboard',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='MSRP',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='brand',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='img',
            field=models.ImageField(null=True, upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mouse',
            name='MSRP',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mouse',
            name='brand',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='mouse',
            name='img',
            field=models.ImageField(null=True, upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='mouse',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mouse',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='phone',
            name='MSRP',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='phone',
            name='brand',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='phone',
            name='img',
            field=models.ImageField(null=True, upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='phone',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]