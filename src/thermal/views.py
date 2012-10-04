import httplib2
import json
import collections

from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

from thermal.models import Stack
from thermal.models import Event
from thermal.forms import make_form

class StackListView(TemplateView):

    template_name = 'stack_list.html'

    def get_context_data(self, **kwargs):
        context = super(StackListView, self).get_context_data(**kwargs)
        context['stacks'] = Stack.objects.all()
        context['menu'] = 1
        return context

class StackDeleteView(TemplateView):
    template_name = 'stack_delete.html'

    def get(self, request, stack_name):
        Stack.delete(stack_name)
        response = HttpResponseRedirect('/heat/stack/')
        return response

class TemplateListView(TemplateView):

    template_name = 'template_list.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateListView, self).get_context_data(**kwargs)

        h = httplib2.Http(".httplib2_cache")
        url = 'https://api.github.com/repos/heat-api/heat/contents/templates'
        resp, content = h.request(url, "GET") 
        templates = json.loads(content)
        templates = map(lambda x: (x['name'], x), templates)
        templates = dict(templates)
        clean = []
        for t in templates:
            if not t.endswith('.template'):
                clean.append(t)
        for t in clean:
            del templates[t]

        templates = templates.keys()
        templates.sort()
        context['templates'] = templates
        context['menu'] = 2
        return context

class TemplateLaunchView(TemplateView):

    template_name = 'template_launch.html'

    def _get_template(self, template_name):
        h = httplib2.Http(".httplib2_cache")
        url = 'https://raw.github.com/heat-api/heat/master/templates/%s'
        url = url % template_name
        resp, content = h.request(url, "GET")
        try:
            # object_pairs_hook requires py2.7
            tmpl_obj = json.loads(content,
                                  object_pairs_hook=collections.OrderedDict)
        except:
            tmpl_obj = json.loads(content)
        return tmpl_obj
    
    def get_context_data(self, template_name, **kwargs):
        context = super(TemplateLaunchView, self).get_context_data(**kwargs)

        t = self._get_template(template_name)
        context['template_name'] = template_name
        context['parameters'] = t['Parameters']
        context['form'] = make_form(t['Parameters'])
        context['menu'] = 2

        return context

    def post(self, request, *args, **kwargs):
        t = self._get_template(kwargs['template_name'])
        result = Stack.launch(t, request.POST.copy())
        response = HttpResponseRedirect('/heat/stack/')
        return response
            
class EventListView(TemplateView):

    template_name = 'event_list.html'

    def get_context_data(self, stack_name=None, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        events = Event.objects.all()
        if stack_name:
            events = events.filter(StackName=stack_name)
        
        context['events'] = events
        context['menu'] = 3
        return context
