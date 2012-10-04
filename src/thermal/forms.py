from django import forms

def make_form(heat_parameters):
    fields = {}
    for param, val in heat_parameters.items():
        if 'AllowedValues' in val:
            choices = map(lambda x: (x,x), val['AllowedValues'])
            fields[param] = forms.ChoiceField(choices=choices)
        else:
            fields[param] = forms.CharField(initial=val.get('Default', None), help_text=val.get('ConstraintDescription', '')) 
        fields[param].initial=val.get('Default', None)
        fields[param].help_text=val.get('Description', '')# + val.get('ConstraintDescription', '')
    return type('HeatTemplateForm',(forms.BaseForm,),{ 'base_fields': fields })
