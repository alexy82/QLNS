# Generated by Django 2.1.4 on 2018-12-11 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuanLyNhaSach', '0007_auto_20181211_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='code',
            field=models.CharField(default='CJECNPIX', max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='stocktransferout',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
