from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.decorators import api_view

from userapp.models import Blog
from rest_framework.viewsets import ViewSet

from .forms import CustomUserForm
from django.contrib import messages
from django.contrib.auth.models import User, Permission
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.generics import ListAPIView

from .serializers import BlogFieldsSerializer, BlogSerializer
from rest_framework import status

from rest_framework.response import Response
from datetime import date
from rest_framework.views import APIView

from rest_framework.decorators import api_view
from rest_framework import mixins, generics
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
        blogs=Blog.objects.all()
        
        # print(user)
         # If the credentials are valid: Returns a User object.
         # If the credentials are invalid: Returns None.
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('admin-dashboard')
            
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

# @login_required(login_url='login')
# def homepage(request):
    # # Fetch all blog objects
    # blogs = Blog.objects.all()

    # # Add the formatted_date for each blog
    # for blog in blogs:
    #     # Format the published_date (you can customize the format here)
    #     blog.formatted_date = blog.published_date.strftime("%Y-%m-%d")

    # return render(request, 'userapp/dashboard.html', {'blogs': blogs})

@login_required(login_url='login')
def adminhomepage(request):
    blogs=Blog.objects.all()
    return render(request,'admin/dashboard.html',{'blogs':blogs})


@login_required
def blogForm(request):
    return render(request,'blog/blog_form.html')


# # using APIView in DRF
# class BlogAPI(APIView):
#     def get(self, request):
#         blogs = Blog.objects.all()
#         serializer = BlogSerializer(blogs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         data = request.data  
#         title = data.get('title')
#         author_name = data.get('author_name')
#         category = data.get('category')
#         description = data.get('description')
#         author_email = data.get('author_email')
#         author_dob = data.get('author_dob')

#         if not all([title, author_name, category, description, author_email, author_dob]):
#             return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

#         blog = Blog.objects.create(
#             title=title,
#             author_name=author_name,
#             category=category,
#             description=description,
#             author_email=author_email.lower(), 
#             author_dob=author_dob,
#             published_date=date.today()
#         )
#         return Response(
#             {
#                 "message": "Blog created successfully.",
#                 "blog": {
#                     "id": blog.id,
#                     "title": blog.title,
#                     "author_name": blog.author_name,
#                     "category": blog.category,
#                     "description": blog.description,
#                     "author_email": blog.author_email,
#                     "author_dob": blog.author_dob,
#                     "published_date": blog.published_date.strftime("%Y-%m-%d"),
#                 },
#             },
#             status=status.HTTP_201_CREATED,
#         )

#     def put(self, request):
#         pass


#     def patch(self, request,blog_id):
#         blog=get_object_or_404(Blog,id=blog_id)
#         blog.title=request.data.get('title')
#         blog.author_name=request.data.get('author_name')
#         blog.category=request.data.get('category')
#         blog.description=request.data.get('description')
#         blog.author_email=request.data.get('author_email')
#         blog.author_dob=request.data.get('author_dob')
#         blog.save()
        
#         return Response(
#             {   
#                 "message": "Blog updated successfully.",
#                 "blog": {
#                     "id": blog.id,
#                     "title": blog.title,
#                     "author_name": blog.author_name,
#                     "category": blog.category,
#                     "description": blog.description,
#                     "author_email": blog.author_email,
#                     "author_dob": blog.author_dob,
#                     "published_date": blog.published_date.strftime("%Y-%m-%d"),
#                 },
#             },
#             status=status.HTTP_201_CREATED,
#         )


#     def delete(self, request,blog_id):
#         if not request.user.has_perm('userapp.delete_blog'):
#             return Response(
#                 {"detail": "You do not have permission to delete blogs."},
#                 status=status.HTTP_403_FORBIDDEN
#             )
#         blog = get_object_or_404(Blog, id=blog_id)

#         blog.delete()
#         return Response(
#             {"detail": "Blog deleted successfully."},
#             status=status.HTTP_204_NO_CONTENT
#         )



# using ViewSet and Default Router
class BlogViewSet(ViewSet):
    def list(self,request):
        blogs=Blog.objects.all()
        serializer=BlogSerializer(blogs,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        blogs=Blog.objects.get(pk=pk)
        serializer=BlogSerializer(blogs)
        return Response(serializer.data)



# # using mixins
class BlogListView(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,generics.GenericAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    def get(self,request):
        return self.list(request)   

    def post(self,request):
        return self.create(request)

    def put(self, request, *args, **kwargs):
            return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




# # Using generic views ( ListAPIView , CreateAPIView ).
# class BlogListView(ListAPIView):
#     queryset=Blog.objects.all()
#     serializer_class=BlogSerializer


# @login_required
# def addBlog(request):
#     if(request.method=='POST'):
#         title=request.POST.get('title')
#         author_name=request.POST.get('author_name')
#         category=request.POST.get('category')
#         description=request.POST.get('description')
#         author_email=request.POST.get('author_email')
#         author_dob=request.POST.get('author_dob')

#         blog=Blog.objects.create(title=title,
#                                  author_name=author_name,
#                                  category=category,
#                                  description=description,
#                                  author_dob=author_dob,
#                                  author_email=author_email,
#                                  published_date=date.today()
#                                  )
#         return redirect('home')
#     return render(request,'masterFile.html')

@login_required
def editBlog(request,blog_id):
    blog=get_object_or_404(Blog,id=blog_id)
    return render(request,'blog/edit_blog.html',{'blog':blog})


# @login_required
# def updateBlog(request,blog_id):
#     blog=get_object_or_404(Blog,id=blog_id)
#     if(request.method=='POST'):
#         blog.title=request.POST.get('title')
#         blog.author_name=request.POST.get('author_name')
#         blog.category=request.POST.get('category')
#         blog.description=request.POST.get('description')
#         blog.save()
#         return redirect('home')

# @login_required
# def deleteBlog(request,blog_id):
#     blog=get_object_or_404(Blog,id=blog_id)
#     blog.delete()
#     return redirect('home')

# @login_required
# def deleteBlog(request, blog_id):
#     if not request.user.has_perm('userapp.delete_blog'):
#         messages.error(request, "You do not have permission to delete blogs.")
#         return redirect('home')  # Adjust 'dashboard' to your actual dashboard URL name

#     blog = get_object_or_404(Blog, id=blog_id)

#     if request.method == "POST":
#         blog.delete()
#         messages.success(request, "Blog deleted successfully.")
#         return redirect('dashboard')

def permissions(request):
    user_permissions = request.user.get_all_permissions()
    return render(request,'userapp/permissions.html',{'permissions':user_permissions})



# @api_view()
# def get_blogs(request):
#     queryset=Blog.objects.all()
#     serializer=BlogSerializer(queryset,many=True)
#     return Response({
#             "data":serializer.data
#         })


# @api_view(["GET"])
# def blogFieldValidation(request):
#     queryset = Blog.objects.all()
#     valid_data = []
#     for blog in queryset:
#         blog_data = {
#             "title": blog.title,
#             "author_name": blog.author_name  
#         }
#         ## this is field level validation check using serializer
#         serializer = BlogFieldsSerializer(data=blog_data)
#         if serializer.is_valid(): 
#             valid_data.append(serializer.data) 
    
#     return Response({
#         "data": valid_data 
#     })
