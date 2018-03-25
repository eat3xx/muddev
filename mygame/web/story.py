# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def storypage(request):
    return render(request, "story.html")