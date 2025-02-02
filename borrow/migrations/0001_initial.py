# Generated by Django 5.0.6 on 2024-07-08 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toy_id', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=20)),
                ('toy_borrow', models.CharField(max_length=20)),
                ('advance_time', models.DateTimeField(auto_now_add=True)),
                ('borrow_time', models.DateTimeField(blank=True, null=True)),
                ('return_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'unique_together': {('toy_id', 'advance_time')},
            },
        ),
    ]
