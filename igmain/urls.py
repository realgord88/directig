from django.contrib import admin
from django.urls import path, include
from igmain import views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^accounts/$', views.IGaccounts.as_view()),
    url(r'^addpublicrival', views.AddPublicRival.as_view()),
    url(r'^delpublicrival', views.DelPublicRival.as_view()),
    url(r'^publicsrival/$', views.IGpublicsRival.as_view()),
    url(r'^publicinfo$', views.InfoAccountPublic.as_view()),
    url(r'^changeaccount', views.ChangeAccount.as_view()),
    url(r'^direct$', views.DirectShare.as_view()),
]

