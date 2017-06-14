# coding:utf-8
from django.shortcuts import render

import django.utils.timezone
# Create your views here.
from django.views.generic import CreateView
from .models import Memo
from django import forms
from django.http import HttpResponseRedirect,HttpResponseForbidden
import datetime
from django.utils import timezone


class MemoForm(forms.Form):
    mid = forms.CharField(widget=forms.HiddenInput(), required=False)
    title = forms.CharField(label=u'标题', error_messages= \
        {'required': u'标题不能为空'}, required=True)

    body = forms.CharField(label=u'内容', error_messages= \
        {'required': u'内容不能为空'}, widget=forms.Textarea( \
        attrs={'rows': 10, 'cols': 40}))

    timestamp = forms.DateTimeField(label=u"时间", error_messages= \
        {'required': u'时间不能为空', 'invalid': u'请输入正确的时间'}, \
        initial=django.utils.timezone.now(),\
        input_formats=["%Y/%m/%d %H:%M:%S"], widget=\
        forms.DateTimeInput(attrs={'placeholder': '时间'}, format="%Y/%m/%d %H:%M:%S"))


def create(request):
    if request.method == "POST":
        form = MemoForm(request.POST)
        if form.is_valid():  # 所有验证都通过
            temp_memo = Memo()
            temp_memo.title = form.cleaned_data['title']
            temp_memo.body = form.cleaned_data['body']
            temp_memo.body.replace("\r\n", "\n").replace("\n", "<br>")
            temp_memo.timestamp = form.cleaned_data['timestamp']
            temp_memo.author = request.user
            temp_memo.save()
            return HttpResponseRedirect("/memo/list/")
    else:
        form = MemoForm(initial={'timestamp': \
                                     django.utils.timezone.now()})
    return render(request, 'memo/memo_form.html', {'form': form})


def edit(request, mid):
    temp_memo = Memo.objects.get(id=int(mid))
    if temp_memo.author != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = MemoForm(request.POST)
        if form.is_valid():  # 所有验证都通过
            temp_memo.title = form.cleaned_data['title']
            temp_memo.body = form.cleaned_data['body']
            temp_memo.body.replace("\r\n", "\n").replace("\n", "<br>")
            temp_memo.timestamp = form.cleaned_data['timestamp']
            temp_memo.author = request.user
            temp_memo.save()
            return HttpResponseRedirect('/memo/list/')
    else:
        form = MemoForm(initial={'body': temp_memo.body.replace("<br>", "\r\n"), \
                                 'timestamp': temp_memo.timestamp, \
                                 "mid": temp_memo.id, \
                                 "title": temp_memo.title})
    return render(request, 'memo/memo_form.html', {'form': form})


def list(request):
    memoes = request.user.memo_set.all()
    return render(request, 'memo/list.html', {'memoes': memoes})
