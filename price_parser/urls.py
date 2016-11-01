from django.conf.urls import url
from .views import *

app_name = 'main_site'
urlpatterns = [
	url(r'^$', ParseView.as_view()),
]
