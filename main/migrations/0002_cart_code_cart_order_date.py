# Generated by Django 5.0.3 on 2024-03-30 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='code',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='order_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
