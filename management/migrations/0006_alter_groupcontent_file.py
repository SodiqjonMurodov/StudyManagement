# Generated by Django 5.0.3 on 2024-05-23 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_groupcontent_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupcontent',
            name='file',
            field=models.FileField(upload_to='files'),
        ),
    ]
