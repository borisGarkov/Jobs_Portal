# Generated by Django 3.2.5 on 2021-08-15 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0012_alter_jobmodel_last_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobmodel',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
