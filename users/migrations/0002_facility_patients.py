# Generated by Django 4.0.4 on 2022-05-14 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='Patients',
            field=models.ManyToManyField(blank=True, null=True, to='users.patient'),
        ),
    ]
