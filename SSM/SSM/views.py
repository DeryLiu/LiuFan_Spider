# encoding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def index(request):
    return redirect('/dashboard/')
