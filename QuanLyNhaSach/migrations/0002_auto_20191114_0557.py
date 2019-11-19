# Generated by Django 2.1 on 2019-11-14 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuanLyNhaSach', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchandise',
            name='picture',
            field=models.CharField(default=None, max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stocktransferout',
            name='status',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='merchandise',
            name='more_info',
            field=models.TextField(blank=True),
        ),
    ]