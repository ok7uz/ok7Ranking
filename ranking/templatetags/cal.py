from django import template
from ranking.functions import calculate
from decimal import Decimal
register = template.Library()

@register.simple_tag(name="calc")
def calculate_points(match, team, g1, g2):
    team1_points = match.team1.points
    team2_points = match.team2.points
    if team == 1:
        return calculate(team1_points, team2_points, g1, g2, match.tournament.coef, match.is_knockout)
    return calculate(team2_points, team1_points, g1, g2, match.tournament.coef, match.is_knockout)

@register.simple_tag(name="win_p")
def winning_probability(points1: Decimal, points2: Decimal):
    dr = points1 - points2
    ex = 1 / (pow(10, -dr / 600) + 1)
    return round(ex * 100)
