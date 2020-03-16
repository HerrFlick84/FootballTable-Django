from . import views 
from django.urls import path
from django.conf.urls import url
urlpatterns = [path(r'',views.startpage),
               path('UpdateResults',views.UpdateResults),
               path('TeamGames',views.TeamGames),
               path('delall',views.delall),
               path('Standings',views.Standings),
               path('Boot',views.Boot),
               ]