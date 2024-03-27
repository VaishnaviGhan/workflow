from django.db import models
from administration.models import Users,Applications,Processes
from checklists.Logdata import logdata

class workflow(models.Model):
    WF_ID = models.AutoField(primary_key=True)
    AppID = models.CharField(max_length=50,null=True,blank=True) # remove
    AppName = models.CharField(max_length=50,null=True,blank=True) # remove
    ProcessID = models.IntegerField(default=1)
    ProcessName = models.ForeignKey(Processes,on_delete=models.CASCADE,default=1)
    Main_model = models.CharField(max_length=50,null=True,blank=True)
    para_1 = models.CharField(max_length=50,null=True,blank=True)
    value_1 = models.CharField(max_length=50,null=True,blank=True)
    para_2 = models.CharField(max_length=50,null=True,blank=True)
    value_2 = models.CharField(max_length=50,null=True,blank=True)
    para_3 = models.CharField(max_length=50,null=True,blank=True)
    value_3 = models.CharField(max_length=50,null=True,blank=True)
    para_4 = models.CharField(max_length=50,null=True,blank=True)
    value_4 = models.CharField(max_length=50,null=True,blank=True)
    para_5 = models.CharField(max_length=50,null=True,blank=True)
    value_5 = models.CharField(max_length=50,null=True,blank=True)
    User_names = models.JSONField(default=list)

    def save(self, *args, **kwargs):
         logdata('record....!')
         logdata(self.ProcessName)
         self.ProcessID = self.ProcessName.ProcessID 
         super().save(*args, **kwargs) 
         return

    def __str__(self):
        return str(self.AppName)
    
class WorkflowLOG(models.Model):
    LogID = models.AutoField(primary_key=True) 
    WF_ID = models.CharField(max_length=70)
    Doc_ID = models.CharField(max_length=70)    # Example Vendor Id
    AppID = models.CharField(max_length=70) 
    AppName = models.CharField(max_length=70)
    ProcessID = models.IntegerField()
    ProcessName = models.CharField(max_length=100)
    CurrentUser = models.CharField(max_length=70) 
    NextUser = models.CharField(max_length=500) 
    Action = models.CharField(max_length=70) 
    DateTimeStamp = models.DateTimeField(auto_now_add=True)
    Comment = models.CharField(max_length=100,null=True,blank=True)


    def __str__(self):
        return str(self.LogID)

class WorkflowInbox(models.Model):
    inbox_id = models.AutoField(primary_key=True)
    Doc_ID = models.CharField(max_length=70)  
    AppID = models.CharField(max_length=70) 
    ProcessID = models.IntegerField()
    CurrentUser = models.CharField(max_length=70) 
    NextUser = models.CharField(max_length=500)
    DateTimeStamp = models.DateTimeField(auto_now_add=True) 


class Approver(models.Model): 
     ApproverID = models.AutoField(primary_key=True)
     ApproverDescription = models.CharField(max_length=100, default='')
     User = models.ForeignKey(Users,on_delete=models.CASCADE)

     def __str__(self):
         return self.ApproverID
