from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views

app_name = 'tobuy'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    # url(r'^additem/$', views.additem, name='additem'),
    url(r'^add_new_list/$', views.add_new_list, name='add_new_list'),
    # url(r'^(?P<pk>[0-9]+)/switch/$', views.switch, name='switch'),
    # url(r'^only_active/$', views.only_active, name='only_active'),
    # url(r'^(?P<pk>[0-9]+)/switch2/$', views.switch2, name='switch2'),
    # url(r'^only_inactive/$', views.only_inactive, name='only_inactive'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^(?P<pk>[0-9]+)/change_active_list/$', views.change_active_list, name='change_active_list'),
    url(r'^invite_user/$', views.invite_user, name='invite_user'),
]