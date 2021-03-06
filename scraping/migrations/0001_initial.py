# Generated by Django 3.1 on 2022-01-20 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announce',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('city', models.CharField(max_length=255)),
                ('date', models.DateTimeField(verbose_name='date')),
                ('type', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255, null=True)),
                ('source', models.CharField(max_length=255)),
                ('original_date', models.CharField(max_length=255)),
                ('original_time', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddConstraint(
            model_name='announce',
            constraint=models.UniqueConstraint(fields=('title', 'city', 'source'), name='title_city_source_unique_constraint'),
        ),
    ]
