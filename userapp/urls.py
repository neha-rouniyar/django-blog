from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet


router = DefaultRouter()
router.register('blogs', BlogViewSet, basename='blog')


urlpatterns = [
    path('api/', include(router.urls)),
    # path('/register',views.register,name='register'),
    # path('/login', views.user_login , name='login'),
    # path('/logout', views.logout, name='logout'),
    # path('/dashboard',views.homepage,name='home'),
    # path('/admin/dashboard',views.adminhomepage,name='admin-dashboard'),


    # # blog post urls
    # path('/blog-form',views.blogForm,name='blog_form'),
    # path('/add-blog',views.addBlog,name='add_blog'),


    # path('/edit-blog/<int:blog_id>',views.editBlog,name='edit_blog'),
    # path('/update-blog/<int:blog_id>',views.updateBlog,name='update_blog'),
    # path('/delete-blog/<int:blog_id>',views.deleteBlog,name='delete_blog'),

    # path('/permissions',views.permissions,name='permissions'),


    # path('/api/blogs/',BlogListView.as_view()),
    # path('/api/blogs/<int:pk>',BlogListView.as_view())

    # # using viewset and Default Router
]