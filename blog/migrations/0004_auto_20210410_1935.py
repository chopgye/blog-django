# Generated by Django 3.1.7 on 2021-04-10 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210408_0303'),
    ]

    operations = [
        migrations.AddField(
            model_name='votemodel',
            name='num_downvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='votemodel',
            name='num_upvotes',
            field=models.IntegerField(default=0),
        ),
    ]
