# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.

from django.http import Http404
from django.shortcuts import render
from django.conf import settings

from evennia.utils.search import object_search
from evennia.utils.utils import inherits_from

def sheet(request, object_id):
    print "sheet"
    object_id = '#' + object_id
    try:
        character = object_search(object_id)[0]
        print "22222"
    except IndexError:
        print "IndexError"
        raise Http404("I couldn't find a character with that ID.")
    if not inherits_from(character, settings.BASE_CHARACTER_TYPECLASS):
        print "not inherit"

        raise Http404("I couldn't find a character with that ID. "
                      "Found something else instead.")
    return render(request, 'character/sheet.html', {'character': character})

def sheet1(request):
    print "sheet1"
    return render(request, 'character/sheet1.html')
    # return render(request, "sheet1.html")
