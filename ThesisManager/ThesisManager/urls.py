"""
URL configuration for ThesisManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import  RedirectView
from django.urls import path
from main import views
from users import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/home/')),
    path('home/', views.home, name='home'),
    path('thesis/', views.thesis_list, name= 'thesis_list'),
    path('thesis/<int:topic_number>/', views.thesis_details, name= 'thesis_details'),    
    path('aboutus/', views.about_us, name= 'about_us'),
    path('create/', views.create_data_campus, name='create_data'),
    path('success/', views.success, name='success'),
    path('login/', user_views.login_user, name='login'),
    path('logout/', user_views.logout_user, name='logout'),
    path('modify/', views.modify, name='CRUD'),
    
    path('test/', views.data_retrieval_test), # for troubleshooting purposes
    # path('previous_data/', views.previous_data),
    # path('add_prev_data/', views.add_previous_data), # add previous given data
    # path('create_user/', user_views.create_new_user), # create users for testing
    # path('create_user/add_permission/', user_views.add_permissions)
]

handler404 = 'main.views.handling_404'
