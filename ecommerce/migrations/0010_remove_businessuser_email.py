# Generated by Django 5.1.3 on 2024-12-10 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0009_remove_order_payment_terms_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessuser',
            name='email',
        ),
    ]
