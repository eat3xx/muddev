from django.conf.urls import url
from web.character.views import sheet, sheet1

urlpatterns = [
    url(r'^sheet/(?P<object_id>\d+)/$', sheet, name="sheet"),
    url(r'^sheet1/$', sheet1, name="sheet1"),
]