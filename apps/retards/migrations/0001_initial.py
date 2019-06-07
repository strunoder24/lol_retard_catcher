# Generated by Django 2.2.2 on 2019-06-07 05:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Retard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='idiot', max_length=100)),
                ('description', models.TextField(blank=True)),
                ('puuid', models.CharField(blank=True, max_length=78)),
                ('summonerLevel', models.PositiveIntegerField(blank=True)),
                ('revisionDate', models.CharField(blank=True, max_length=100)),
                ('summonerId', models.CharField(max_length=63)),
                ('accountId', models.CharField(max_length=56)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]