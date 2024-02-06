from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from datetime import date

from ranking.models import *


class MainSitemap(Sitemap):
    changefreq = "hourly"
    priority = 1.0
    lastmod = date.today()

    def items(self):
        return ['home', 'matches', 'fixtures', 'stats', 'calculator', 'privacy', 'about']

    def location(self, item):
        return reverse(item)


class PageSitemap(Sitemap):
    changefreq = "hourly"
    priority = 1.0
    lastmod = date.today()

    def items(self):
        return list(range(2, 6))

    def location(self, item):
        return reverse('home') + f'?page={item}'


class CountrySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    lastmod = date.today()

    def items(self):
        return Team.objects.all()

    def location(self, item):
        return reverse('country', args=[item.short_name])


class ConfSitemap(Sitemap):
    changefreq = "hourly"
    priority = 1.0
    lastmod = date.today()

    def items(self):
        return CONFS

    def location(self, item):
        return reverse('home') + f'?conf={item}'
