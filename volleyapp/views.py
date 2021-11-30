from django.shortcuts import get_object_or_404, redirect, render,get_list_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.generic.base import View
from .forms import CreateScoreForm, PlayerChoiceForm
from django.forms import modelformset_factory
from .models import Teamname, Playername, Playerscores
from .graph import Output_Graph,Plot_Graph_attack,Plot_Graph_receive,Plot_Graph_effect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.db.models import F
import collections
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import datetime
import numpy as np
from django.urls import reverse
from urllib.parse import urlencode


# Create your views here.
def signupfunc(request):
  if request.method == "POST":
    username = request.POST['username']
    emailaddress = request.POST['emailaddress']
    password = request.POST['password']
    if not password:
      return render(request, 'signup.html',{'error':'パスワードを入力してください'})
    elif not emailaddress:
       return render(request, 'signup.html',{'error':'メールアドレスを入力してください'})
    else:
      try:
        user = User.objects.create_user(username, emailaddress, password)
        return redirect('login')
      except IntegrityError:
        return render(request, 'signup.html',{'error':'このユーザーは登録されています。'})
  return render(request, 'signup.html',{})

def loginfunc(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'login.html',{'context':'loginに失敗しました。'})
  return render(request, 'login.html',{})

def logoutfunc(request):
  logout(request)
  return redirect('login')

@login_required
def homefunc(request):
  object = Teamname.objects.all()
  return render(request, 'home.html',{'object':object})

@login_required
def teamlistfunc(request):
  object = Teamname.objects.filter(user=request.user.id)
  # object = Teamname.objects.all()
  # print(object.team)
  return render(request, 'teamlist.html',{'object':object})

@login_required
def listfunc(request, pk):
  teamname = get_object_or_404(Teamname, pk=pk)
  object_list = teamname.playername_set.all()
  return render(request, 'list.html',{'object_list':object_list , 'teamname':teamname})

@login_required
def createteamfunc(request):
  if request.method == 'POST':
    object = Teamname.objects.create(user=request.user, team = request.POST['team'])
    object.save()
    return redirect('teamlist')
  else:
    return render(request, 'createteam.html')

@login_required
def createplayerfunc(request, pk):
  if request.method == 'POST':
    # object_list = 
    teamname = get_object_or_404(Teamname, pk=pk)
    object = Playername.objects.create(team = teamname,name = request.POST['name'])
    object.save()
    return redirect('list',pk)
  else:
    return render(request, 'createplayer.html')

@login_required
def scoresfunc(request, pk):
  # 選手特定
  playername = get_object_or_404(Playername, pk=pk)
  # チーム特定
  teamname = playername.team
  # 特定した選手のスコアをすべて出す。
  scores = playername.playerscores_set.all()
  # 計算に使う値の取り出し(numpy型)
  # 今までのスパイク決定数すべて出す
  spike_success_n = np.array([score.spike_success for score in scores])
  # スパイク決めない数すべて
  spike_not_success_n = np.array([score.spike_not_success for score in scores])
  # レシーブ成功数すべて
  receive_success_n = np.array([score.receive_success for score in scores])
  # レシーブ失敗数すべて
  receive_not_success_n = np.array([score.receive_not_success for score in scores])
  # サーブ効果なし数すべて
  serve_not_effect_n = np.array([score.serve_not_effect for score in scores])
  # ノータッチエース数すべて
  Notouch_ace_n = np.array([score.Notouch_ace for score in scores])
  # サービスエース数すべて
  ace_n = np.array([score.ace for score in scores])
  # サーブ効果本数のすべて
  effect_n = np.array([score.effect for score in scores])
  # 決定率、返却率、サーブ効果率を計算
  # 決定率
  attack_decision_rate_n = spike_success_n / (spike_success_n + spike_not_success_n)
  # 返却率
  receive_rate_n = receive_success_n / (receive_success_n + receive_not_success_n)
  # サーブ効果率
  effect_rate_n = ((Notouch_ace_n*100)+(ace_n*80)+(effect_n*25))/(serve_not_effect_n+Notouch_ace_n+ace_n+effect_n)

  # リストに戻す
  attack_decision_rate_list = attack_decision_rate_n.tolist()
  receive_rate_list = receive_rate_n.tolist()
  effect_rate_list = effect_rate_n.tolist()

  # 四捨五入（丸め）（5→0、5.1→10)
  attack_decision_rate_list = [round(num, 2) for num in attack_decision_rate_list]
  receive_rate_list = [round(num, 2) for num in receive_rate_list]
  effect_rate_list = [round(num, 2) for num in effect_rate_list]
  
  # グラフのパラメータ
  # 決定率
  y_attack = attack_decision_rate_list
  # 最近のデータ10個をグラフ化
  y_attack = y_attack[-10:]
  x_attack = list(range(1,len(y_attack)+1))
  chart_attack = Plot_Graph_attack(x_attack,y_attack)  
  # 返球率
  y_receive = receive_rate_list
  y_receive = y_receive[-10:]
  x_receive = list(range(1,len(y_receive)+1))
  chart_receive = Plot_Graph_receive(x_receive,y_receive)
  # 効果率
  y_effect = effect_rate_list
  y_effect = y_effect[-10:]
  x_effect = list(range(1,len(y_effect)+1))
  chart_effect = Plot_Graph_effect(x_effect,y_effect)
  # 日にち 
  dates = [score.date for score in scores]
  dates = dates[-10:]

  return render(request, 'scores.html',{
    'playername':playername,
    'teamname':teamname,
    'y_attack':y_attack,
    'y_receive':y_receive,
    'y_effect':y_effect,
    'chart_attack':chart_attack, 
    'chart_receive':chart_receive,
    'chart_effect':chart_effect,
    'dates':dates
    })

@login_required
def allscorefunc(request, pk):
  # scorefuncと同じく全スコアをリスト化
  # 選手特定
  playername = get_object_or_404(Playername, pk=pk)
  # チーム特定
  teamname = playername.team
  # 特定した選手のスコアをすべて出す。
  scores = playername.playerscores_set.all()
  # 計算に使う値の取り出し(numpy型)
  # 今までのスパイク決定数すべて出す
  spike_success_n = np.array([score.spike_success for score in scores])
  # スパイク決めない数すべて
  spike_not_success_n = np.array([score.spike_not_success for score in scores])
  # レシーブ成功数すべて
  receive_success_n = np.array([score.receive_success for score in scores])
  # レシーブ失敗数すべて
  receive_not_success_n = np.array([score.receive_not_success for score in scores])
  # サーブ効果なし数すべて
  serve_not_effect_n = np.array([score.serve_not_effect for score in scores])
  # ノータッチエース数すべて
  Notouch_ace_n = np.array([score.Notouch_ace for score in scores])
  # サービスエース数すべて
  ace_n = np.array([score.ace for score in scores])
  # サーブ効果本数のすべて
  effect_n = np.array([score.effect for score in scores])
  # 決定率、返却率、サーブ効果率を計算
  # スパイク本数
  spike_num = spike_success_n + spike_not_success_n
  # 決定率
  attack_decision_rate_n = spike_success_n / spike_num
  # レシーブ本数
  receive_num = receive_success_n + receive_not_success_n
  # 返却率
  receive_rate_n = receive_success_n / receive_num
  # サーブ本数
  serve_num = serve_not_effect_n+Notouch_ace_n+ace_n+effect_n
  # サーブ効果率
  effect_rate_n = ((Notouch_ace_n*100)+(ace_n*80)+(effect_n*25))/serve_num

  # リストに戻す
  attack_decision_rate_list = attack_decision_rate_n.tolist()
  receive_rate_list = receive_rate_n.tolist()
  effect_rate_list = effect_rate_n.tolist()

  # 四捨五入（丸め）（5→0、5.1→10)
  attack_decision_rate_list = [round(num, 2) for num in attack_decision_rate_list]
  receive_rate_list = [round(num, 2) for num in receive_rate_list]
  effect_rate_list = [round(num, 2) for num in effect_rate_list]

  return render(request, 'allscore.html',{
  'playername':playername,
  'teamname':teamname,
  'scores':scores,
  'spike_num':spike_num,
  'receive_num':receive_num,
  'serve_num':serve_num,
  'attack_decision_rate_list':attack_decision_rate_list,
  'receive_rate_list':receive_rate_list,
  'effect_rate_list':effect_rate_list,
  })

@login_required
def deletescorefunc(request, pk):
  object = Playerscores.objects.filter(pk=pk)
  if request.method == 'POST':
      object.delete()
      return redirect('home')
  else:
      return render(request, 'deletescore.html', {'object':object})


@login_required
def deleteplayerfunc(request, pk):
    object = Playername.objects.filter(pk=pk)
    playername = get_object_or_404(Playername, pk=pk)
    if request.method == 'POST':
        object.delete()
        return redirect('teamlist')
    else:
        return render(request, 'deleteplayer.html', {'playername':playername})

@login_required
def deleteteamfunc(request, pk):
    object = Teamname.objects.filter(pk=pk)
    teamname = get_object_or_404(Teamname, pk=pk)
    if request.method == 'POST':
        object.delete()
        return redirect('teamlist')
    else:
        return render(request, 'deleteteam.html', {'teamname':teamname})

@login_required
def scoresteamlistfunc(request):
  object = Teamname.objects.filter(user=request.user.id)
  # object = Teamname.objects.all()
  # print(object.team)
  return render(request, 'scoretemplate/scoreteamlist.html',{'object':object})

@login_required
def scoreplayerlistfunc(request,pk):
  teamname = get_object_or_404(Teamname, pk=pk)
  object_list = teamname.playername_set.all()
  return render(request, 'scoretemplate/scoreplayerlist.html',{'object_list':object_list , 'teamname':teamname})


# 記入する選手を選ぶ
@login_required
def scorechoicefunc(request,pk):
  teamname = get_object_or_404(Teamname, pk=pk)
  object_list = teamname.playername_set.all()
  form = PlayerChoiceForm(request.POST or None)
  form.fields['name'].queryset = object_list
  if request.method == 'POST' and form.is_valid():
    names = form.cleaned_data.get('name')
    print(names)
    request.session['names'] = names
    return redirect('scoreplayerlist', pk=pk)

  else:
    return render(request,'scoretemplate/scorechoice.html',{'form':form})

# スコアを書くfunc
# 全員分同時に書く
@login_required
def createscorefunc(request, pk):
  names = request.session['names']
  teamname = get_object_or_404(Teamname, pk=pk)
  players = names
  CreateScoreFormSet = modelformset_factory(model=Playerscores, form=CreateScoreForm, extra=len(players))
  initial = [{'name' : names,'date':datetime.date.today()} for names in players]
  formset = CreateScoreFormSet(request.POST or None, queryset=Playerscores.objects.none(), initial=initial)
  if request.method == 'POST' and formset.is_valid():
    formset.save()
    return redirect('scoreplayerlist',pk=pk)
  else:
    context = {
      'teamname':teamname,
      'formset': formset,
      'players' : players
    }
    return render(request, 'scoretemplate/scoreplayerlist.html',context)
