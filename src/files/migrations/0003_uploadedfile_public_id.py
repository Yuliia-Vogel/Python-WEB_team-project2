# Generated by Django 5.1.6 on 2025-02-25 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_remove_uploadedfile_file_uploadedfile_file_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='public_id',
            field=models.CharField(default=999, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
