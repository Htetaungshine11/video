# Generated by Django 3.1.5 on 2021-07-01 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tst', '0002_auto_20210701_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='name',
            field=models.CharField(default='', max_length=200, unique=True),
        ),
    ]
