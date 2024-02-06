from django import template
from ranking.functions import *

register = template.Library()

@register.simple_tag(name="calc")
def function(match, team, g1, g2):
    if team == 1:
        return calculate(match.team1.points, match.team2.points, g1, g2, match.tournament.coef, match.is_knockout)
    return calculate(match.team2.points, match.team1.points, g1, g2, match.tournament.coef, match.is_knockout)

@register.simple_tag(name="win_p")
def win_p(points1: Decimal, points2: Decimal):
    dr = points1 - points2
    ex = 1 / (pow(10, -dr / 600) + 1)

    return round(ex * 100) 