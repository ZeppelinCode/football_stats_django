# Generated by Django 2.2 on 2019-04-28 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.IntegerField(unique=True)),
                ('city', models.CharField(max_length=255, null=True)),
                ('stadium', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.IntegerField(unique=True)),
                ('match_time_utc', models.DateTimeField(null=True)),
                ('league_name', models.CharField(max_length=255, null=True)),
                ('viewers', models.IntegerField(null=True)),
                ('last_update_utc', models.DateTimeField(null=True)),
                ('finished', models.BooleanField(default=False)),
                ('matchday', models.IntegerField(null=True)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='matches.Location')),
                ('team_1', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fk_team_1', to='teams.Team')),
                ('team_2', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fk_team_2', to='teams.Team')),
            ],
        ),
        migrations.CreateModel(
            name='MatchDayMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchday', models.IntegerField()),
                ('last_update', models.DateTimeField()),
            ],
            options={
                'db_table': 'matches_matchday_metadata',
            },
        ),
        migrations.CreateModel(
            name='Outcome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outcome_type', models.CharField(max_length=4)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='matches.Match')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teams.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.IntegerField(unique=True)),
                ('goal_getter_name', models.CharField(max_length=255)),
                ('match_minute', models.IntegerField(null=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='matches.Match')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teams.Team')),
            ],
        ),
        migrations.AddConstraint(
            model_name='outcome',
            constraint=models.CheckConstraint(check=models.Q(outcome_type__in=['win', 'loss', 'draw']), name='chk_outcome_type'),
        ),
        migrations.AddIndex(
            model_name='match',
            index=models.Index(fields=['team_1'], name='matches_mat_team_1__dc1885_idx'),
        ),
        migrations.AddIndex(
            model_name='match',
            index=models.Index(fields=['team_2'], name='matches_mat_team_2__3bedd0_idx'),
        ),
    ]
