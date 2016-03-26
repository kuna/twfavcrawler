from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^api/testtwit/$', views.api_testtwit),
]
