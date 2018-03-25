"""
Url definition file to redistribute incoming URL requests to django
views. Search the Django documentation for "URL dispatcher" for more
help.

"""
from django.conf.urls import url, include

# default evennia patterns
from evennia.web.urls import urlpatterns

# eventual custom patterns
from web import story

custom_patterns = [
    # url(r'/desired/url/', view, name='example'),
    url(r'^story', story.storypage),
    url(r'^c1', story.storypage),
    url(r'^character/', include('web.character.urls',namespace='character', app_name='character')),
    url(r'^chargen/', include('web.chargen.urls')),
]

# this is required by Django.
urlpatterns = custom_patterns + urlpatterns
