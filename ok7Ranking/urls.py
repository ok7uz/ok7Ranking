from django.conf import settings
from django.views.static import serve
from django.views.generic import RedirectView, TemplateView

from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('ads.txt/', TemplateView.as_view(template_name='ads.txt', content_type="text/plain"), name='ads'),
    path('',  include('ranking.urls'))
] 
urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {
        "document_root": settings.MEDIA_ROOT}),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico'))
]
