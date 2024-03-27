#------------New adventure-------------
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from administration.models import Applications,Processes,Users
from .models import workflow,WorkflowLOG,Approver,WorkflowInbox
from checklists.Logdata import logdata
import dev.config as cfg 
from django.db.models import Max

class WORKFLOW():
    def __init__(self,AppID=0):
        self.ProcessID = ""
        self.ProcessName = ""
        self.Doc_ID = 0
        self.AppID = AppID
        self.AppName = ""
        self.FormData = {}
        self.Expression1 = ""
        self.Expression2 = ""
        self.UserList = []
        self.CurrentUser = ""
        self.action = cfg.Approve
        self.Comment = ""
        self.WF_ID = 0
        self.NextUser = ""
        self.getProcessID()
        return
    
    def getProcessID(self):
        application = Applications.objects.values().filter(AppID=self.AppID)[0]
        self.ProcessID = application['ProcessName_id']
        self.ProcessName = Processes.objects.values().filter(ProcessID=self.ProcessID)[0]['ProcessName']
        self.AppName = application['AppName'].strip()
        return
    
    def SelectWorkFlow(self,AppID):
        rows = workflow.objects.values().filter(ProcessID=self.ProcessID)
        for row in rows:
            result = self.CreateEXP(row)
            if result:
                self.WF_ID = row['WF_ID']
                self.UserList = row['User_names'] 

                #break 
        if self.WF_ID == 0:
            self.NextUser = self.CurrentUser
        else:
            if self.action == cfg.Approve:
                approver_instance = Approver.objects.get(User__username=self.CurrentUser)
                approver_id = approver_instance.ApproverID
                logdata('ak-ak')
                logdata(approver_id)
                found_one = False

                for item in self.UserList:
                    if isinstance(item, list):
                        for i in item:
                            if i == approver_id:
                                found_one = True
                                if found_one is True:
                                    iDX = self.UserList.index(item)
                                    print(iDX)
                                    if iDX == len(self.UserList)-1:
                                     next_ele = self.UserList[iDX]
                                     usernames = []
                                     for usr in next_ele:
                                        next_user = Approver.objects.get(ApproverID=usr)
                                        usernames.append(next_user.User.username)
                                     self.NextUser = usernames
                                     print('mocambo in sublist and and that sublist is at last index of main list',self.NextUser)
                                    else:
                                        next_ele = self.UserList[iDX+1]
                                        print('mocambo is in inbetween sublist and next element is = ',next_ele)
                                        # next_ele = self.UserList[iDX]
                                        if isinstance(next_ele, list):
                                            usernames = []
                                            for usr in next_ele:
                                                next_user = Approver.objects.get(ApproverID=usr)
                                                usernames.append(next_user.User.username)
                                            self.NextUser = usernames
                                            print('login user present in list and next element also a list and next hero"s are',self.NextUser)
                                        else:
                                            nextuserID = Approver.objects.get(ApproverID=next_ele)
                                            nextusername = nextuserID.User
                                            self.NextUser = nextusername.username
                                 
                                break  # Exit the loop once 1 is found in the nested list
                    elif item == approver_id:
                        found_one = True
                        if found_one is True:
                            iDX = self.UserList.index(item)
                            #****** 22 march
                           
                            #****** 22 march
                            if iDX == len(self.UserList)-1:
                             next_ele = self.UserList[iDX]
                             if isinstance(next_ele, list):
                                usernames = []
                                for usr in next_ele:
                                    next_user = Approver.objects.get(ApproverID=usr)
                                    usernames.append(next_user.User.username)
                                self.NextUser = usernames
                             else:
                                nextuserID = Approver.objects.get(ApproverID=next_ele)
                                nextusername = nextuserID.User.username
                                self.NextUser = nextusername
                                print('mocambo is last member and next_ele is = ',self.NextUser)
                            else:
                                next_ele = self.UserList[iDX+1]
                                if isinstance(next_ele, list):
                                    usernames = []
                                    for usr in next_ele:
                                        next_user = Approver.objects.get(ApproverID=usr)
                                        usernames.append(next_user.User.username)
                                    self.NextUser = usernames
                                    print('Harisankul',self.NextUser)
                                    print('mocambo in between somewhere',self.NextUser)
                                else:
                                    nextuserID = Approver.objects.get(ApproverID=next_ele)
                                    nextusername = nextuserID.User.username
                                    self.NextUser = nextusername

                        break  # Exit the loop once 1 is found in the main list

                if found_one:
                    print('Approver is is present')
                else:
                    next_ele = self.UserList[0]
                    if isinstance(next_ele, list):
                        usernames = []
                        for usr in next_ele:
                            next_user = Approver.objects.get(ApproverID=usr)
                            usernames.append(next_user.User.username)
                        self.NextUser = usernames
                    else:
                        nextuserID = Approver.objects.get(ApproverID=next_ele)
                        nextusername = nextuserID.User.username
                        self.NextUser = nextusername
                        print('mocambo not present in workflow list and next _ele is ',self.NextUser)
                        print('approver id  is not present')

            if self.action == cfg.Reject:
                approver_instance = Approver.objects.get(User__username=self.CurrentUser)
                approver_id = approver_instance.ApproverID
                found_one = False
                
                for item in self.UserList:  
                    if isinstance(item, list): #[1,[3,4,5],[6,7,8],9]
                        for i in item:
                            if i == approver_id:
                                found_one = True
                                if found_one is True:
                                    iDX = self.UserList.index(item) #2
                                    if iDX > 0:
                                        next_ele = self.UserList[iDX-1]# [4,5,6] #[3,4,5]
                                        if isinstance(next_ele, list): 
                                            usernames = []
                                            for usr in next_ele:
                                                next_user = Approver.objects.get(ApproverID=usr)
                                                usernames.append(next_user.User.username)
                                            self.NextUser = usernames
                                        else:
                                            nextuserID = Approver.objects.get(ApproverID=next_ele)
                                            nextusername = nextuserID.User.username
                                            self.NextUser = nextusername
                                    else:
                                        workflowLOGrows = WorkflowLOG.objects.values().filter(Doc_ID=self.Doc_ID,ProcessID=self.ProcessID).order_by('LogID')
                                        self.NextUser = workflowLOGrows[0]['CurrentUser']
                                        userid = Users.objects.get(username=self.NextUser)
                                        nextuserID = Approver.objects.get(User=userid)
                                        nextusername = nextuserID.User
                                        self.NextUser = nextusername.username
                                        print('login user present in sublist and at first position so that previous user after rekection is = ',type(self.NextUser))
                            break  # Exit the loop once 1 is found in the nested list
                    
                    if item == approver_id and self.UserList.index(approver_id) > 0:
                        found_one = True
                        if found_one is True:
                            iDX = self.UserList.index(item)
                            next_ele = self.UserList[iDX-1]
                            if isinstance(next_ele, list):
                                usernames = []
                                for usr in next_ele:
                                    next_user = Approver.objects.get(ApproverID=usr)
                                    usernames.append(next_user.User.username)
                                self.NextUser = usernames
                                print('mocambo in between somewhere',self.NextUser)
                            else:
                                nextuserID = Approver.objects.get(ApproverID=next_ele)
                                nextusername = nextuserID.User.username
                                self.NextUser = nextusername
                        break  # Exit the loop once 1 is found in the main list
                    
                    if item== approver_id and self.UserList.index(approver_id) == 0 : 
                    #********** IF USER IS NOT PRESENT IN WORKFLOW USERLIST **********
                        workflowLOGrows = WorkflowLOG.objects.values().filter(Doc_ID=self.Doc_ID,ProcessID=self.ProcessID).order_by('LogID')
                        self.NextUser = workflowLOGrows[0]['CurrentUser']
                        logdata(self.NextUser)
                        userid = Users.objects.get(username=self.NextUser)
                        logdata(userid)
                        nextuserID = Approver.objects.get(User=userid)
                        nextusername = nextuserID.User.username
                        self.NextUser = nextusername
                        logdata(self.NextUser)
                        break
        return
       
    def CreateEXP(self,row):
        self.Expression1 = ""
        self.Expression2 = ""
        
        if row['para_1'] != None and row['para_1'] != "":
            self.Expression1 = self.Expression1 + row['para_1'].strip() + "=" + str(row['value_1']) + " and " 
            self.Expression2 = self.Expression2 + row['para_1'].strip() + "=" + str(self.FormData[row['para_1'].strip()]) + " and " 
        
        if row['para_2'] != None and row['para_2'] != "":
            self.Expression1 = self.Expression1 + row['para_2'].strip() + "=" + str(row['value_2']) + " and " 
            self.Expression2 = self.Expression2 + row['para_2'].strip() + "=" + str(self.FormData[row['para_2'].strip()]) + " and " 
           
        if row['para_3'] != None and row['para_3'] != "":
            self.Expression1 = self.Expression1 + row['para_3'].strip() + "=" + str(row['value_3']) + " and " 
            self.Expression2 = self.Expression2 + row['para_3'].strip() + "=" + str(self.FormData[row['para_3'].strip()]) + " and " 
           
        if row['para_4'] != None and row['para_4'] != "":
            self.Expression1 = self.Expression1 + row['para_4'].strip() + "=" + str(row['value_4']) + " and " 
            self.Expression2 = self.Expression2 + row['para_4'].strip() + "=" + str(self.FormData[row['para_4'].strip()]) + " and " 
            
        if row['para_5'] != None and row['para_5'] != "":
            self.Expression1 = self.Expression1 + row['para_5'].strip() + "=" + str(row['value_5']) + " and " 
            self.Expression2 = self.Expression2 + row['para_5'].strip() + "=" + str(self.FormData[row['para_5'].strip()]) + " and " 

        self.Expression1 = self.Expression1.strip(' and ')
        self.Expression2 = self.Expression2.strip(' and ')
        if self.Expression1 == self.Expression2:
            
             return True

        return False

def mydocuments(request):
    #Inbox_Docs = WorkflowInbox.objects.filter(NextUser=request.user) NextUser__icontains
    Inbox_Docs = WorkflowInbox.objects.filter( NextUser__icontains=request.user) 
    inbox_count = WorkflowInbox.objects.filter(NextUser=request.user).count()
    workflow_info = []

    for record in Inbox_Docs:
        app_link = Applications.objects.get(AppID=record.AppID).AppLink
        app_discription = Applications.objects.get(AppID=record.AppID).AppName
        installedApp = Applications.objects.get(AppID=record.AppID).InstalledApp
        inbox_url = Applications.objects.get(AppID=record.AppID).inbox_url
        process_name = Processes.objects.get(pk=record.ProcessID).ProcessName   # Define this function to get process name
        logdata(record.ProcessID)
        
        url = f'{inbox_url}/{record.Doc_ID}/'
        workflow_info.append({
            'Doc_ID': record.Doc_ID,
            'AppLink': app_link,  # Assuming AppLink is the same as AppName in the Applications model
            'AppDesc':app_discription,
            'installedApp':installedApp,
            'ProcessName': process_name,
            'CurrentUser': record.CurrentUser,
            'NextUser': record.NextUser,
            'DateTimeStamp': record.DateTimeStamp,
            'url':url,
           
        })
    context = { 
                'app_title': 'Add country',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'app_title':'Add country',
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'workflow_info':workflow_info,
                
                }        

    return render(request, 'workflow/MyDocument.html', context)