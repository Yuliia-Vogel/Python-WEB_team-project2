# Generated by Django 5.1.6 on 2025-02-23 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedfile',
            name='file',
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='file_url',
            field=models.URLField(default=7665),
            preserve_default=False,
        ),
    ]
