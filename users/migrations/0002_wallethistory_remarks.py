# Generated by Django 3.1.6 on 2021-02-22 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallethistory',
            name='remarks',
            field=models.TextField(null=True),
        ),
    ]
