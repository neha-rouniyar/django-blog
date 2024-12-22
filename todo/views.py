from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Task

def homapage(request):
    tasks=["Learn Django","Learn Client Communication","Learn Python","Learn React"]
    return render(request , 'index.html',{'tasks':tasks})

def task_form(request):
    return render(request, 'tasks/insert_tasks_form.html')

def insert_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        task=Task(title=title,description=description)
        task.save()

        # Save to database (if needed)
        return HttpResponse(f"Task '{title}' added successfully!")
    else:
        return HttpResponse("Invalid Request", status=400)
    
def view_tasks(request):
    tasks=Task.objects.all()
    return render(request,'tasks/view_tasks.html',{'tasks':tasks})

def edit_task(request,task_id):
    task=get_object_or_404(Task,id=task_id)
    return render(request,'tasks/edit_task.html',{'task':task})

def update_task(request,task_id):
    task=get_object_or_404(Task,id=task_id)
    if(request.method=='POST'):
        task.title=request.POST.get('title')
        task.description=request.POST.get('description')
        task.save()
        return render(request,'tasks/view_tasks.html')

def delete_task(request,task_id):
    task=get_object_or_404(Task,id=task_id)
    task.delete()
    task.save()

    return HttpResponse("Deletion successfully")