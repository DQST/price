from django.conf.urls import url
from .views import *


app_name = 'main_site'
urlpatterns = [
    url(r'^$', SearchView.as_view()),
    url(r'^upload/$', ImportView.as_view()),
    url(r'^ajax/$', AjaxView.as_view()),
    url(r'^fast/$', FastSearchView.as_view()),
    url(r'^cat/$', CategoryView.as_view()),
]
