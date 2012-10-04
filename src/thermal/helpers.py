import xml.etree.ElementTree as etree

from heat import client as heat_client

### Heat Client

def format_parameters(self, params):
    parameters = {}
    print params
    for count, p in enumerate(params, 1):
        parameters['Parameters.member.%d.ParameterKey' % count] = p
        parameters['Parameters.member.%d.ParameterValue' % count] = params[p]
    return parameters

heat_client.HeatClient.format_parameters = format_parameters

def get_heat_client():
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

### XML Parsing

def get_members(xml):
    root = etree.fromstring(xml)
    return root.findall('.//member')
