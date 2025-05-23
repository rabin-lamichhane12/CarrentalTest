# Generated by Django 5.2 on 2025-04-13 09:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('car_type', models.CharField(choices=[('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Hatchback', 'Hatchback'), ('Pickup', 'Pickup')], max_length=20)),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=6)),
                ('image', models.ImageField(upload_to='car_images/')),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_date', models.DateField()),
                ('return_date', models.DateField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental.car')),
            ],
        ),
    ]
