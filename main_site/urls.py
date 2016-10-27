from django.conf.urls import url
from .views import *


app_name = 'main_site'
urlpatterns = [
    url(r'^$', SearchView.as_view()),
    url(r'^upload/$', ImportView.as_view()),
    url(r'^parse/$', ParseView.as_view()),
    url(r'^ajax/$', AjaxView.as_view()),
    url(r'^fast/$', FastView.as_view()),
]
