# Generated by Django 4.2.3 on 2024-04-18 18:12

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
            name='GameSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game_sessions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_bot', models.BooleanField(default=False)),
                ('pits', models.JSONField(default=list)),
                ('kazan', models.JSONField(default=list)),
                ('tuzdyq', models.JSONField(default=list)),
                ('game_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_histories', to='togyzkumalak.gamesession')),
            ],
        ),
    ]
