from django.db import models
from datetime import datetime, timedelta, timezone
from django.contrib.auth.models import User

# Create your models here.
class Teamname(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  team = models.CharField(max_length=10000)
  def __str__(self):
    return str(self.team)

class Playername(models.Model):
  team = models.ForeignKey(Teamname, on_delete=models.CASCADE)
  name = models.CharField(max_length=10000)
  def __str__(self):
    return str(self.name)

class Playerscores(models.Model):
  name = models.ForeignKey(Playername, on_delete=models.CASCADE)
  # スパイク決定率
  # attackdecisionrate = models.DecimalField(verbose_name='',max_digits=2,decimal_places=2,blank=True,null=True,default=0.00)
  # レシーブ返球率
  # returnrate = models.DecimalField(verbose_name='',max_digits=2,decimal_places=2,blank=True,null=True,default=0.00)
  # スパイク決定打数
  spike_success=models.PositiveIntegerField()
  #スパイク決めない数
  spike_not_success=models.PositiveIntegerField()
  # レシーブ返却数
  receive_success=models.PositiveIntegerField()
  # レシーブミス
  receive_not_success=models.PositiveIntegerField()
  # ブロック本数/１セット
  block_success=models.PositiveIntegerField()
  # サーブ効果なし数
  serve_not_effect=models.PositiveIntegerField()
  # ノータッチエース数
  Notouch_ace=models.PositiveIntegerField()
  #サービスエース数
  ace=models.PositiveIntegerField()
  # サーブ効果
  effect=models.PositiveIntegerField()
  # 相手チーム入力
  opponent=models.CharField(blank=True,null=True,max_length=50)
  # 日付
  date = models.DateField()
  def __str__(self):
    return str(self.name)
