from django.db.models import F, Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page

from ranking.models import *


def get_teams(conf=None):
    teams = Team.objects.only(
        'rank', 'conf_rank', 'short_name', 'name', 'flag', 'points', 'previous_points',
        'previous_rank', 'previous_conf_rank'
    ).annotate(
        points_change=F('points') - F('previous_points'),
        rank_change=F('rank') - F('previous_rank'),
        conf_rank_change=F('conf_rank') - F('previous_conf_rank'),
    )

    if conf:
        if conf not in CONFS:
            return None

        teams = teams.filter(conf=conf).annotate(
            rank_change=F('conf_rank') - F('previous_conf_rank'),
        )

    return teams

@cache_page(1)
def home_view(request):
    conf = request.GET.get('conf')
    page_number = request.GET.get("page")

    teams = get_teams(conf)

    if teams is None:
        return redirect('home_view')
    
    paginator = Paginator(teams, 50)
    teams = paginator.get_page(page_number)

    if page_number and int(page_number) > paginator.num_pages:
        return redirect('home')

    return render(request, 'home.html', {
        'teams': teams,
        'confs': CONFS,
        'paginator': paginator,
    })


@cache_page(300)
def matches_view(request):
    page_number = request.GET.get("page")
    matches = Match.objects.filter(goal1__isnull=False).order_by('-date', 'tournament')

    paginator = Paginator(matches, 25)
    matches = paginator.get_page(page_number)

    if page_number and int(page_number) > paginator.num_pages:
        return redirect('matches')

    return render(request, 'matches.html', {
        'matches': matches,
        'paginator': paginator,
    })



@cache_page(300)
def fixtures_view(request):
    fixtures = Match.objects.filter(goal1__isnull=True).order_by('date', 'tournament')

    return render(request, 'fixtures.html', {
        'matches': fixtures,
    })


@cache_page(60 * 5)
def country_view(request, country):
    team = Team.objects.all().annotate(
        points_change=F('points') - F('previous_points'),
        rank_change=F('rank')-F('previous_rank'),
        conf_rank_change=F('conf_rank')-F('previous_conf_rank'),
    ).filter(short_name=country).first()
   
    if not team:
        return redirect('home')

    matches = Match.objects.filter(Q(team1=team) | Q(team2=team)).order_by('-date')

    return render(request, 'country.html', {
        'team': team,
        'matches': matches,
    })


@cache_page(300)
def stats_view(request):
    teams = Team.objects.all().annotate(
        points_change=F('points') - F('previous_points'),
        rank_change=F('rank')-F('previous_rank'),
    )

    best_teams = teams.filter(rank_change__lt=0).order_by('rank_change')[:10]
    best_teams_by_points = teams.filter(points_change__gt=0).order_by('-points_change')[:10]
    worst_teams = teams.filter(rank_change__gt=0).order_by('-rank_change')[:10]
    worst_teams_by_points = teams.filter(points_change__lt=0).order_by('points_change')[:10]

    return render(request, 'stats.html', {
        'best_teams': best_teams,
        'best_teams_by_points': best_teams_by_points,
        'worst_teams': worst_teams,
        'worst_teams_by_points': worst_teams_by_points,
    })


@cache_page(300)
def calculator_view(request):
    fixtures = Match.objects.filter(goal1__isnull=True).order_by('date', 'tournament')

    return render(request, 'calculator.html', {
        'matches': fixtures,
    })
