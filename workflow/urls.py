from django.urls import path
from . import views,workflow


urlpatterns = [

    path('addworkflow/',views.workflowpro,name='addworkflow'),
    path('editworkflow//<int:pk>/',views.editworkflow,name='editworkflow'),
    path('workflowlist/',views.workflowlist,name='workflowlist'),
    path('a/',views.GetModelFieldsByAppName),
    path('logicworkflow/',views.workflowlogic,name='logicworkflow'),

    path('approver_list/', views.approver_list, name='approver_list'),
    path('add_approver/', views.add_approver, name='add_approver'),
    path('edit_approver/<int:pk>/', views.edit_approver, name='edit_approver'),
    path('delete_approver/<int:pk>/', views.delete_approver, name='delete_approver'), 
    #path('mydocuments/',workflow.mydocuments,name="mydocuments"),
    path('mydocuments/',workflow.mydocuments,name='mydocuments'),
   
]


