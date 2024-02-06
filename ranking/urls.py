from django.urls import path
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView

from ranking import views
from ranking.sitemap import *

sitemaps = {
    'main_urls': MainSitemap,
    'main_pages': PageSitemap,
    'confs': ConfSitemap,
    'countries': CountrySitemap,
}

urlpatterns = [
    path('',  views.home_view, name='home'),
    path('matches/',  views.matches_view, name='matches'),
    path('fixtures/',  views.fixtures_view, name='fixtures'),
    path('stats/',  views.stats_view, name='stats'),
    path('country/<slug:country>/', views.country_view, name='country'),
    path('calculator/', views.calculator_view, name='calculator'),
]

urlpatterns += [
    path('sitemap', sitemap, {'sitemaps': sitemaps}),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
