from decimal import Decimal

CONFS = ['uefa', 'caf', 'conmebol', 'concacaf', 'afc', 'ofc']
CONF_CHOICES = ((conf, conf) for conf in CONFS)


def calculate(points1: Decimal, points2: Decimal,
              goal1, goal2, coef, is_knockout=False, is_penalty=False, gp1=None, gp2=None):
    dr = points1 - points2
    ex = 1 / (pow(10, -dr / 600) + 1)

    w = 1 if goal1 > goal2 else 0 if goal1 < goal2 else 0.75 if is_penalty and gp1 > gp2 else 0.5
    w = Decimal(w)

    points_change = coef * (w - ex)
    if is_knockout:
        points_change = max(0, points_change)

    return round(points_change, 2) 


def ranking(team_model):
    teams = team_model.objects.all().order_by('-points')

    for i in range(len(teams)):
        team = teams[i]
        team.rank = i + 1
        team.save()
    
    for conf in CONFS:
        i = 1
    
        for team in teams:
            if team.conf == conf:
                team.conf_rank = i
                team.save()
                i += 1
