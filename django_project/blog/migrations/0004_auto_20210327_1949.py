# Generated by Django 3.1.7 on 2021-03-27 19:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_auto_20210327_1947'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BlogComment',
            new_name='Comment',
        ),
    ]