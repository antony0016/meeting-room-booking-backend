# Generated by Django 4.0 on 2022-01-04 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PopMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('text', models.TextField()),
                ('redirect_url', models.TextField(blank='')),
                ('object_id', models.IntegerField(blank='')),
            ],
        ),
    ]
