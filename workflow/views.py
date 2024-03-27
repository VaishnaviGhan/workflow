from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from django.http import JsonResponse
from .forms import workflow1Form,ApproverForm
from .models import workflow,Approver,WorkflowLOG
from checklists.Logdata import logdata
from django.apps import apps
from checklists.models import CheckList_Trans_Header
from django.db import models
from administration.models import Applications
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import inspect
import dev.config as cfg
from administration.authlib import CheckAuthorization

def workflowpro(request):
    if request.method == 'POST':
        form = workflow1Form(request.POST)
        logdata(form.errors)
        if form.is_valid():
            logdata(form.errors)
            form.save()
            logdata(form.errors)
            return redirect('workflowlist')
    else:
        form = workflow1Form()
    
    context = {
        'app_title': 'Application List',
        'username': request.user.get_full_name(),
        'isActive': request.user.is_authenticated,
        'isSuperUser': request.user.is_superuser,
        'app_title': 'Workflow',
        'isForm': True,
        'isHomePage': True,
        'form': form,    
    }

    return render(request, 'workflow/workflow.html',context)


def workflowlist(request):
    WFList = workflow.objects.all().order_by('WF_ID')
    context = {
        'app_title': 'Application List',
        'username': request.user.get_full_name(),
        'isActive': request.user.is_authenticated,
        'isSuperUser': request.user.is_superuser,
        'app_title': 'Workflow List',
        'isForm': True,
        'isHomePage': True,
        'WFList':WFList
        
    }

    return render(request, 'workflow/workflow.html',context)

def editworkflow(request, pk):       
    WFList = workflow.objects.all().order_by('WF_ID')
    if request.method == 'POST':
        work = workflow.objects.get(WF_ID=pk)
        form = workflow1Form(request.POST, instance=work)
        if form.is_valid():
           form.save()
           messages.info(request,'workflow edited successfully')
           return redirect('workflowlist')
        else:
            messages.warning(request, 'Something went wrong! Please check form input.')
            return redirect('workflowlist')        
    else:
        work = workflow.objects.get(WF_ID=pk)
        form = workflow1Form(instance=work)
        context = { 'form' : form,
                    'app_title': 'Edit Application',
                    'username': request.user.get_full_name(), 
                    'isActive' : request.user.is_authenticated,
                    'isSuperUser' : request.user.is_superuser,
                    'app_title':'Edit Application',
                    'isForm' : True,
                    'isHomePage' : True,
                  
                    'WFList' : WFList,
                  }          
    return render(request, 'workflow/workflow.html', context)  


def GetModelFieldsByAppName(AppName):
    AppDetails = Applications.objects.filter(AppName=AppName).values()
    ModelName = AppDetails[0]['ModelName']
    InstalledApp = AppDetails[0]['InstalledApp']
    ThisModel = apps.get_model(InstalledApp, ModelName)
    
    ModelFields = []
    for field in ThisModel._meta.get_fields():
        logdata(field)
        if field.model != ThisModel:
           
            continue  # Skip fields not belonging to the current model
            
        ModelFields.append(field.name.upper())
        
    return ModelFields

def workflowlogic(request):
    ModelFields = []
    for field in workflow._meta.get_fields():
     ModelFields.append(field.name)
    return HttpResponse(ModelFields)

def approver_list(request):
    approvers = Approver.objects.all()
    context = { 'app_title': 'Application List',
                'username': request.user.get_full_name(),
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'app_title':'Application List',
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'approvers' : approvers,
                }       
    return render(request, 'workflow/approver.html', context)

def add_approver(request):
    AppName = inspect.stack()[0][3].strip()
    AppID = cfg.Apps[AppName]
    UserID = request.user.UserID
    if not CheckAuthorization(AppID=AppID, UserID=UserID):
        messages.info(request,'You are not authorized for this application')
        return redirect('/administration/approver_list/')
    approvers=Approver.objects.all()
    if request.method == "POST":
        form = ApproverForm(request.POST)
        if form.is_valid():
            approver = form.save(commit=False)
            approver.save()
            messages.success(request, 'Approver created successfully.')
            return redirect('approver_list')
    else:
        form = ApproverForm()
    context = { 'form' : form,
                    'app_title': 'Add Approver',
                    'username': request.user.get_full_name(),
                    'isActive' : request.user.is_authenticated,
                    'isSuperUser' : request.user.is_superuser,
                    'app_title':'Add Approver',
                    'isForm' : True,
                    'isHomePage' : True,
                    'company_name' : cfg.CompanyName,
                    'approvers' : approvers,
                  }
    return render(request, 'workflow/approver.html', context)

def edit_approver(request, pk):
    AppName = inspect.stack()[0][3].strip()
    AppID = cfg.Apps[AppName]
    UserID = request.user.UserID
    if not CheckAuthorization(AppID=AppID, UserID=UserID):
        messages.info(request,'You are not authorized for this application')
        return redirect('/administration/approver_list/')
    approvers=Approver.objects.all()
    approver = get_object_or_404(Approver, pk=pk)
    if request.method == "POST":
        form = ApproverForm(request.POST, instance=approver)
        if form.is_valid():
            approver = form.save(commit=False)
            approver.save()
            messages.success(request, 'Approver updated successfully.')
            return redirect('approver_list')
    else:
        form = ApproverForm(instance=approver)
    context = { 'form' : form,
                'app_title': 'Edit Approver',
                'username': request.user.get_full_name(),
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'app_title':'Edit Approver',
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'approvers' : approvers,
                }
    return render(request, 'workflow/approver.html', context)

def delete_approver(request, pk):
    AppName = inspect.stack()[0][3].strip()
    AppID = cfg.Apps[AppName]
    UserID = request.user.UserID
    if not CheckAuthorization(AppID=AppID, UserID=UserID):
        messages.info(request,'You are not authorized for this application')
        return redirect('/administration/approver_list/')
    approver = get_object_or_404(Approver, pk=pk)
    approver.delete()
    messages.success(request, 'Approver Deleted successfully.')
    return redirect('approver_list')

