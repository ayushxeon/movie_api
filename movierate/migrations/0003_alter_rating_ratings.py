# Generated by Django 4.0.4 on 2022-04-28 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movierate', '0002_rename_movie_title_movie_movie_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='ratings',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
