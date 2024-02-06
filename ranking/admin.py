from django.contrib import admin
from django.utils.html import format_html

from ranking.models import *


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('rank_display', 'flag_image', 'name', 'points_display', 'conf')
    list_display_links = ('name', 'flag_image')
    list_filter = ('conf',)
    search_fields = ('name',)

    fields = ('name', 'flag', 'rank_display', 'points_display', 'conf', 'conf_rank', 'previous_conf_rank')
    readonly_fields = ('rank_display', 'points_display', 'conf')

    def rank_display(self, obj):
        change = obj.previous_rank - obj.rank
        html = f'<b>{obj.rank}</b> '

        if change > 0:
            html += '(<span style="color: green">+{}</span>)'
        elif change < 0:
            html += '(<span style="color: red">{}</span>)'
        else:
            pass

        return format_html(html, change)

    def points_display(self, obj):
        change = obj.points - obj.previous_points
        html = f'<b>{obj.points}</b> '

        if change > 0:
            html += '(<span style="color: green">+{}</span>)'
        elif change < 0:
            html += '(<span style="color: red">{}</span>)'
        else:
            pass

        return format_html(html, change)

    def flag_image(self, obj):
        html = f'<img style="border: 1px solid black; border-radius: 10%" src="{obj.flag.url}" width=30>'

        return format_html(html)

    rank_display.short_description = 'rank'
    points_display.short_description = 'points'


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('flag1', 'team1', 'score', 'team2', 'flag2',)
    list_display_links = ('flag1', 'flag2')
    list_filter = ('date',)
    list_per_page = 20
    search_fields = ('team1', 'team2')

    def flag1(self, obj):
        html = f'<img style="border: 1px solid black; border-radius: 10%" src="{obj.team1.flag}" width=30>'

        return format_html(html)

    def flag2(self, obj):
        html = f'<img style="border: 1px solid black; border-radius: 10%" src="{obj.team2.flag}" width=30>'

        return format_html(html)

    def score(self, obj):
        if obj.goal1 is not None:
            html = f'<b>{obj.goal1} - {obj.goal2}</b>'
        else:
            html = f'{obj.date}'

        return format_html(html)


admin.site.register(Tournament)
