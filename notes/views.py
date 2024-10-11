from django.shortcuts import render,redirect

from django.views.generic import View

from notes.forms import TaskForm

from notes.models import Task

from django.contrib import messages

from django import forms



class TaskCreateView(View):
    def get(self,request,*args,**kwargs):

        form_instance=TaskForm()


        return render(request,"task_create.html",{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        form_instance=TaskForm(request.POST)

        if form_instance.is_valid():     
            # data=form_instance.changed_data

            # qs=Task.objects.create(**data)

            form_instance.save()

            messages.success(request,"task has been added")

            return redirect("task-list")
        else:
            messages.error(request,"task has not been added")
            return render(request,"task_create.html",{"form":form_instance})

        


class TaskListView(View):

    def get(self,request,*args,**kwargs):

        qs=Task.objects.all()

        return render(request,"task_list.html",{"task":qs})


class TaskDetailView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Task.objects.get(id=id)

        return render(request,"task_detail",{"task":qs})

    

class TaskUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Task.objects.get(id=id)

        form_instance=TaskForm(instance=qs)

        # adding status field to form_instance

        form_instance.fields["status"]=forms.ChoiceField(choices=Task.status_choices,widget=forms.Select(attrs={"class":"form-control form-select"}))

        return render(request,"task_update.html",{"form":form_instance})
    

    
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        form_instance=TaskForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            # extract status from request.POST
            status=request.POST.get("status")

            qs=Task.objects.filter(id=id).update(**data,status=status)

            return redirect("task-list")
        

        else:
            
            return render(request,"task_update.html",{"form":form_instance})
        
       

class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        qs=Task.objects.get(id=id).delete()
        return redirect("task-list")





class TaskSummaryView(View):
    def get(self,request,*args,**kwargs):
        qs=Task.objects.all()

        total_task_count=qs.count()
        
        return render(request,"task_summary.html",{ "total_task_count":total_task_count})

        

        
