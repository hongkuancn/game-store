# Generated by Django 2.1.5 on 2019-02-15 20:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20190215_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boughtgame',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='games.Player'),
        ),
    ]
