from django.contrib import admin
from django.urls import path, include
from .views import  signupfunc, loginfunc, logoutfunc, homefunc, teamlistfunc, listfunc, createteamfunc, scoresfunc, createplayerfunc,deleteplayerfunc, deletescorefunc, deleteteamfunc, scoresteamlistfunc, scorechoicefunc, scoreplayerlistfunc, createscorefunc, allscorefunc

urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/',loginfunc, name='login'),
    path('logout',logoutfunc, name='logout'),
    path('list/<int:pk>', listfunc, name='list'),
    path('', homefunc, name='home'),
    path('teamlist/', teamlistfunc, name='teamlist'),
    path('createteam/', createteamfunc, name='createteam'),
    path('createplayer/<int:pk>',createplayerfunc,name="createplayer"),
    path('scores/<int:pk>', scoresfunc, name= 'scores'),
    path('deleteplayer/<int:pk>', deleteplayerfunc, name='deleteplayer'),
    path('deleteteam/<int:pk>', deleteteamfunc, name='deleteteam'),
    path('scoretemplate/scoreteamlist',scoresteamlistfunc, name='scoreteamlist'),
    path('scoretemplate/scorechoice/<int:pk>',scorechoicefunc, name="scorechoice"),
    path('scoretemplate/scoreplayerlist/<int:pk>', createscorefunc, name='scoreplayerlist'),
    path('allscore/<int:pk>', allscorefunc, name='allscore'),
    path('deletescore/<int:pk>', deletescorefunc, name='deletescore')
]
