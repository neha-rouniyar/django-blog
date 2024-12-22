from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from userapp.models import Blog
from .forms import CustomUserForm
from django.contrib import messages
from django.contrib.auth.models import User, Permission
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Assign required permissions
            add_permission = Permission.objects.get(codename='add_blog')
            change_permission = Permission.objects.get(codename='change_blog')

            user.user_permissions.add(add_permission, change_permission)

            messages.success(request, "Registration successful! You have permissions to add and edit blogs.")
            return redirect('login')  # Adjust as needed
    else:
        form = CustomUserForm()

    return render(request, 'userapp/register.html', {'form': form})


def user_login(request):
    form = CustomUserForm(request.POST)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # print(user)
         # If the credentials are valid: Returns a User object.
         # If the credentials are invalid: Returns None.
        
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'userapp/login.html', context = {
        "form": form
    })

def logout(request):
    request.session.flush() 
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  

@login_required(login_url='login')
def homepage(request):
    blogs=Blog.objects.all()
    return render(request,'userapp/dashboard.html',{'blogs':blogs})

@login_required
def blogForm(request):
    return render(request,'blog/blog_form.html')

@login_required
def addBlog(request):
    if(request.method=='POST'):
        title=request.POST.get('title')
        author_name=request.POST.get('author_name')
        category=request.POST.get('category')
        description=request.POST.get('description')

        blog=Blog.objects.create(title=title,author_name=author_name,category=category,description=description)
        return redirect('home')
    return render(request,'userapp/dashboard.html')

@login_required
def editBlog(request,blog_id):
    blog=get_object_or_404(Blog,id=blog_id)
    return render(request,'blog/edit_blog.html',{'blog':blog})


@login_required
def updateBlog(request,blog_id):
    blog=get_object_or_404(Blog,id=blog_id)
    if(request.method=='POST'):
        blog.title=request.POST.get('title')
        blog.author_name=request.POST.get('author_name')
        blog.category=request.POST.get('category')
        blog.description=request.POST.get('description')
        blog.save()
        return redirect('home')

# @login_required
# def deleteBlog(request,blog_id):
#     blog=get_object_or_404(Blog,id=blog_id)
#     blog.delete()
#     return redirect('home')

@login_required
def deleteBlog(request, blog_id):
    if not request.user.has_perm('userapp.delete_blog'):
        messages.error(request, "You do not have permission to delete blogs.")
        return redirect('home')  # Adjust 'dashboard' to your actual dashboard URL name

    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog deleted successfully.")
        return redirect('dashboard')

def permissions(request):
    user_permissions = request.user.get_all_permissions()
    return render(request,'userapp/permissions.html',{'permissions':user_permissions})