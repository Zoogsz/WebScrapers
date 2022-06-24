# Generated by Django 4.0.5 on 2022-06-24 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('link', models.CharField(default='', max_length=2083, unique=True)),
                ('published', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('source', models.CharField(blank=True, default='', max_length=30, null=True)),
            ],
        ),
    ]