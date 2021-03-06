# Generated by Django 3.0.7 on 2020-08-28 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(max_length=80, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(blank=True),
        ),
    ]
