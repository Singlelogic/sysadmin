# Generated by Django 3.0.4 on 2020-05-26 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20200525_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='name',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
