from django import forms
from django.forms import widgets
from django.forms import formset_factory
from django.forms.models import fields_for_model
from . import models
from .models import Playername,Teamname,Playerscores
from django.shortcuts import get_object_or_404, redirect, render,get_list_or_404

# class CustomModelChoiceField(forms.ModelChoiceField):
#     def label_from_instance(self, obj): # label_from_instance 関数をオーバーライド
#          return obj.name # 表示したいカラム名を return

class PlayerChoiceForm(forms.ModelForm):
    name = forms.ModelMultipleChoiceField(
        queryset=Playername.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Playername
        fields = ('name',)



class CreateScoreForm(forms.ModelForm):
    date = forms.DateField(
        label='日付',
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=['%Y-%m-%d'])

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = Playerscores
        fields = ('name','spike_success', 'spike_not_success', 'receive_success', 'receive_not_success', 'block_success', 'serve_not_effect', 'Notouch_ace', 'ace', 'effect', 'date',"opponent")
        widgets = {
            'name':forms.HiddenInput(),
        }
        
