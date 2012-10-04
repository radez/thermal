import sys
import gettext
import cherrypy
import httplib2
import json
import base64
import xml.etree.ElementTree as ET

# setup jinja2
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

sys.path.append('/home/dradez/workspace/git/heat/')
gettext.install('heat', unicode=1)
from heat import client as heat_client

xml_declaration = '''<?xml version="1.0" encoding="ISO-8859-1"?>
<?xml-stylesheet type="text/xsl" href="%s"?>
'''

### Decorators
def mimetype(type):
    def decorate(func):
        def wrapper(*args, **kwargs):
            cherrypy.response.headers['Content-Type'] = type
            return func(*args, **kwargs)
        return wrapper
    return decorate

def xslt(stylesheet):
    def decorate(func):
        def wrapper(*args, **kwargs):
            xml_decl = xml_declaration % stylesheet
            return xml_decl + func(*args, **kwargs)
        return wrapper
    return decorate

### Heat Client

def format_parameters(self, params):
    parameters = {}
    print params
    for count, p in enumerate(params, 1):
        parameters['Parameters.member.%d.ParameterKey' % count] = p
        parameters['Parameters.member.%d.ParameterValue' % count] = params[p]
    return parameters

heat_client.HeatClient.format_parameters = format_parameters

def get_client():
    """
    Returns a new client object to a heat server
    specified by the --host and --port options
    supplied to the CLI
    """
    options = {'host':'localhost',
	       'port':8000,
	       'username':'admin',
	       'password':'verybadpass',
	       'tenant':'admin',
	       'auth_url':'http://127.0.0.1:5000/v2.0/',
	       'auth_strategy':None,
	       'auth_token':'d57638a3cced1564cc0d',
	       'region':None,
	       'insecure':False,
              }
    return heat_client.get_client(**options)

### CherryPy Objects
class Stack(object):
    templates = None

    @cherrypy.expose
    @mimetype('text/xml')
    @xslt('/xslt/heat_wui_stack_list.xsl')
    def list(self):
        c = get_client()
        result = c.list_stacks()
        return result

    @cherrypy.expose
    def delete(self, stackname):
        parameters = {'StackName': stackname}
        c = get_client()
        result = c.delete_stack(**parameters)
        return result

    @cherrypy.expose
    def create(self, template=None, **kwargs):
        method = cherrypy.request.method.upper()
        context = {}

        h = httplib2.Http(".httplib2_cache")
        if self.templates == None:
            url = 'https://api.github.com/repos/heat-api/heat/contents/templates'
            resp, content = h.request(url, "GET") 
            self.templates = json.loads(content)
            self.templates = map(lambda x: (x['name'], x), self.templates)
            self.templates = dict(self.templates)
            clean = []
            for t in self.templates:
                if not t.endswith('.template'):
                    clean.append(t)
            for t in clean:
                del self.templates[t]

        if template:
            tmpl = env.get_template('create.html')
            url = self.templates[template]['_links']['self']
            resp, content = h.request(url, "GET")
            c = json.loads(content)
            heat_template = base64.b64decode(c['content'])
            t = json.loads(heat_template)
            context['parameters'] = t['Parameters']

        if method == 'POST':
            parameters = {'StackName': kwargs['StackName'],
                          'TimeoutInMinutes': 5,
                          'TemplateBody': heat_template,
                         }
            # get the form params
            c = get_client()
            params_to_format = {}
            for p in context['parameters']:
                if p in kwargs:
                    params_to_format[p] = kwargs[p]
            parameters.update(c.format_parameters(params_to_format))
            print parameters
            result = c.create_stack(**parameters)
            return result
            
        else:

            if not template:
                tmpl = env.get_template('create_list_templates.html')
                templates = self.templates.keys()
                templates.sort()
                context['templates'] = templates
        return tmpl.render(**context)

class Event(object):
    @cherrypy.expose
    @mimetype('text/xml')
    @xslt('/xslt/heat_wui_event_list.xsl')
    def list(self, stackname=None):
        parameters = {'StackName': stackname}

        c = get_client()
        result = c.list_stack_events(**parameters)
        return result

class Root(object):
    stack = Stack()
    event = Event()

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render()

    @cherrypy.expose
    @mimetype('text/xsl')
    def xslt(self, xslt):
        tmpl = env.get_template('xsl/%s' % xslt)
        return tmpl.render()

cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(Root())
