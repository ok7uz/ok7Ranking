from django.db import models

from ranking.functions import *


class Team(models.Model):
    name = models.CharField(max_length=64)
    short_name = models.CharField(primary_key=True, max_length=3)

    flag = models.URLField(max_length=200)
    conf = models.CharField(choices=CONF_CHOICES, max_length=8)

    previous_rank = models.IntegerField()
    rank = models.IntegerField(blank=True)

    previous_conf_rank = models.IntegerField(blank=True)
    conf_rank = models.IntegerField(blank=True)

    points = models.DecimalField(decimal_places=2, max_digits=6, blank=True)
    previous_points = models.DecimalField(decimal_places=2, max_digits=6)

    class Meta:
        indexes = [
            models.Index(fields=['conf']),
            models.Index(fields=['name']),
        ]
        ordering = ('rank',)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=64)
    coef = models.IntegerField()

    def __str__(self):
        return self.name


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    date = models.DateField()

    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')

    goal1 = models.IntegerField(blank=True, null=True)
    goal2 = models.IntegerField(blank=True, null=True)

    is_knockout = models.BooleanField(default=False)
    is_penalty = models.BooleanField(default=False)

    goal1_pen = models.IntegerField(null=True, blank=True)
    goal2_pen = models.IntegerField(null=True, blank=True)

    points1_change = models.DecimalField(decimal_places=2, max_digits=6, blank=True, null=True)
    points2_change = models.DecimalField(decimal_places=2, max_digits=6, blank=True, null=True)

    class Meta:
        ordering = ('date',)

    def save(self, *args, **kwargs):
        if self.goal1 is None:
            return super().save(force_insert=False, *args, **kwargs)

        points1_change = calculate(
            self.team1.points, self.team2.points,
            self.goal1, self.goal2,
            self.tournament.coef, self.is_knockout, self.is_penalty,
            self.goal1_pen, self.goal2_pen
        )
        points2_change = calculate(
            self.team2.points, self.team1.points,
            self.goal2, self.goal1,
            self.tournament.coef, self.is_knockout, self.is_penalty,
            self.goal2_pen, self.goal1_pen
        )

        self.points1_change = points1_change
        self.points2_change = points2_change

        self.team1.points += points1_change
        self.team2.points += points2_change
        
        Team.objects.bulk_update([self.team1, self.team2], ['points'])

        ranking(Team)

        return super().save(force_insert=False, *args, **kwargs)

    def delete(self, using=None, keep_parents=False):

        if not (self.points1_change or self.points2_change):
            return super().delete()

        self.team1.points -= self.points1_change
        self.team1.save()

        self.team2.points -= self.points2_change
        self.team2.save()

        ranking(Team)

        super().delete()

    def __str__(self):
        return (f'{self.team1} {self.goal1 if self.goal1 is not None else ''} - '
                f'{self.goal2 if self.goal2 is not None else ''} {self.team2}')
