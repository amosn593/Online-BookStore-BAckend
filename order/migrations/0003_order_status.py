# Generated by Django 4.0.2 on 2022-03-02 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_order_stripe_token_remove_order_zipcode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='Pending', max_length=15, null=True),
        ),
    ]
