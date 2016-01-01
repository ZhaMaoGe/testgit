from django.conf.urls import url
from . import views
app_name='demo'
urlpatterns=[
	url(r'^index/$',views.index),
	url(r'^$',views.index,name='index'),
	url(r'^login/$',views.login,name='login'),
	url(r'^system/$',views.system,name='system'),
	url(r'^logout/$',views.logout,name='logout'),
	url(r'^craptimer/$',views.craptimer,name='craptimer'),
	url(r'^crap/$',views.crap,name='crap'),
	url(r'^crap_begin/$',views.crap_begin,name='crap_begin'),
	url(r'^upweb/$',views.upweb,name='upweb'),
	url(r'^query/$',views.query,name="query"),
	url(r'^analysis/$',views.analysis,name="analysis"),
	]