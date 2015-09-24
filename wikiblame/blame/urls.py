from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.point, name='point'),
	url(r'^point$', views.point, name='point'),
	url(r'^finger$', views.finger, name='finger'),
]