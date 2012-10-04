from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

from thermal.views import StackListView
from thermal.views import StackDeleteView
from thermal.views import EventListView
from thermal.views import TemplateListView
from thermal.views import TemplateLaunchView

urlpatterns = patterns('',
    #url(r'^$', TemplateView.as_view(template_name="index.html"), name='home'),
    url(r'^stack/$', StackListView.as_view(), name='stack_list'),
    url(r'^stack/(?P<stack_name>[^/]*)/delete/$', StackDeleteView.as_view(), name='stack_delete'),
    url(r'^event/$', EventListView.as_view(), name='event_list'),
    url(r'^event/(?P<stack_name>[^/]*)/$', EventListView.as_view(), name='stack_event_list'),
    url(r'^template/$', TemplateListView.as_view(), name='template_list'),
    url(r'^template/(?P<template_name>[^/]*)/$', TemplateLaunchView.as_view(), name='template_launch'),
)
