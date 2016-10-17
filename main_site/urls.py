from django.conf.urls import url
from .views import SearchView, ImportView, ParseView


app_name = 'main_site'
urlpatterns = [
    url(r'^$', SearchView.as_view()),
    url(r'^upload/$', ImportView.as_view()),
    url(r'^parse/$', ParseView.as_view())
]
