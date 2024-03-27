from django.contrib import admin
from .models import workflow,WorkflowLOG,WorkflowInbox

# # Register your models here.
# class adminworkflow(admin.ModelAdmin):
#     list_display = ['appli_name','models_name','fields_names']
# admin.site.register(workflow,adminworkflow)


class adminworkflow1(admin.ModelAdmin):
     list_display = ['AppID','AppName','Main_model','para_1','value_1','para_2','value_2','para_3','value_3','para_4','value_4','para_5','value_5']
admin.site.register(workflow,adminworkflow1)


class adminWorkflowLOG(admin.ModelAdmin):
     list_display = ['LogID','WF_ID','Doc_ID','AppID','AppName','ProcessID','ProcessName','CurrentUser','NextUser','Action','DateTimeStamp','Comment']

admin.site.register(WorkflowLOG,adminWorkflowLOG)


class adminWorkflowInbox(admin.ModelAdmin):
     list_display = ['inbox_id','Doc_ID','AppID','ProcessID','CurrentUser','NextUser','DateTimeStamp']

admin.site.register(WorkflowInbox,adminWorkflowInbox)
