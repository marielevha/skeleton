# Generated by Django 3.1 on 2022-01-15 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='announce',
            old_name='lien',
            new_name='link',
        ),
    ]
