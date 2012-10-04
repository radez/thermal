class HeatClient(object):
    def format_parameters(self, params):
        raise "overload this function"

    def list_stacks(self):
        return _get_xml('heat/stack_list.xml')

    def list_stack_events(self):
        return _get_xml('heat/event_list.xml')

def _get_xml(file_name):
    return open(file_name).read()

def get_client(**kwargs):
    return HeatClient()
