# Generated by Django 2.1.4 on 2019-02-18 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20190215_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_profile_picture',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='game',
            name='url_link',
            field=models.URLField(max_length=500),
        ),
    ]
