# Generated by Django 3.0.7 on 2020-06-14 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('uid', models.IntegerField(primary_key=True, serialize=False)),
                ('uname', models.CharField(max_length=20)),
                ('pwd', models.CharField(max_length=20)),
                ('fname', models.CharField(max_length=20)),
                ('lname', models.CharField(max_length=20)),
                ('mob', models.IntegerField()),
                ('email', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('age', models.IntegerField()),
                ('romantic', models.CharField(max_length=20)),
                ('action', models.CharField(max_length=20)),
                ('comedy', models.CharField(max_length=20)),
                ('animation', models.CharField(max_length=20)),
                ('horror', models.CharField(max_length=20)),
            ],
        ),
    ]