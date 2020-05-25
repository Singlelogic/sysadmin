# Generated by Django 3.0.4 on 2020-05-23 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20200523_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='title',
            field=models.CharField(db_index=True, default=None, max_length=150),
        ),
        migrations.AlterField(
            model_name='images',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='blog.Post'),
        ),
    ]
