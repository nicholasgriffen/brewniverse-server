# Generated by Django 2.1.4 on 2018-12-13 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brewser',
            name='channels',
            field=models.ManyToManyField(to='posts.Tag'),
        ),
    ]