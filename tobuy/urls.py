from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views

app_name = 'tobuy'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add_new_list/$', views.add_new_list, name='add_new_list'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^(?P<pk>[0-9]+)/change_active_list/$', views.change_active_list, name='change_active_list'),
    url(r'^invite_user/$', views.invite_user, name='invite_user'),
]