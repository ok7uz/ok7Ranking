# Generated by Django 5.0.1 on 2024-01-30 05:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('coef', models.IntegerField()),
                ('image', models.ImageField(upload_to='tours/')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('name', models.CharField(max_length=64)),
                ('short_name', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('flag', models.ImageField(upload_to='flags/')),
                ('conf', models.CharField(choices=[('uefa', 'uefa'), ('caf', 'caf'), ('conmebol', 'conmebol'), ('concacaf', 'concacaf'), ('afc', 'afc'), ('ofc', 'ofc')], max_length=8)),
                ('previous_rank', models.IntegerField()),
                ('rank', models.IntegerField(blank=True)),
                ('previous_conf_rank', models.IntegerField(blank=True)),
                ('conf_rank', models.IntegerField(blank=True)),
                ('points', models.DecimalField(blank=True, decimal_places=2, max_digits=6)),
                ('previous_points', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
            options={
                'ordering': ('rank',),
                'indexes': [models.Index(fields=['conf'], name='ranking_tea_conf_0929a4_idx'), models.Index(fields=['name'], name='ranking_tea_name_7ae292_idx')],
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('goal1', models.IntegerField(blank=True, null=True)),
                ('goal2', models.IntegerField(blank=True, null=True)),
                ('is_knockout', models.BooleanField(default=False)),
                ('is_penalty', models.BooleanField(default=False)),
                ('goal1_pen', models.IntegerField(blank=True, null=True)),
                ('goal2_pen', models.IntegerField(blank=True, null=True)),
                ('points1_change', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('points2_change', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_matches', to='ranking.team')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_matches', to='ranking.team')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='ranking.tournament')),
            ],
            options={
                'ordering': ('date',),
            },
        ),
    ]
