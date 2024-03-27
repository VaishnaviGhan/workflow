from django import forms
from django.apps import apps
from .models import workflow,Approver
from checklists.Logdata import logdata
from administration.models import Applications,Processes
from workflow import config as cfg

class workflow1Form(forms.ModelForm):
    class Meta:
        model = workflow
        fields = ['AppID','AppName','ProcessName','para_1','value_1','para_2','value_2','para_3','value_3','para_4','value_4','para_5','value_5','User_names']

        labels = {
            'para_1': 'Parameter 1',
            'para_2': 'Parameter 2',
            'para_3': 'Parameter 3',
            'para_4': 'Parameter 4',
            'para_5': 'Parameter 5',
        }

class ApproverForm(forms.ModelForm):
    class Meta:
        model = Approver
        fields = ['ApproverDescription', 'User']