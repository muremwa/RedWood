# Generated by Django 2.1.2 on 2019-01-10 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='art',
            field=models.ImageField(blank=True, null=True, upload_to='watch/art/'),
        ),
    ]
