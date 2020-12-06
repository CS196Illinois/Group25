from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('standings/', views.standings, name="standings"),
    path('<str:team_searched>/', views.search, name="search"),
]