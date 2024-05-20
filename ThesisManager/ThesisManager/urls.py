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
    path('', RedirectView.as_view(url='home')),
    path('home/', views.home, name='home'),
    path('thesis/', views.thesis_list, name= 'thesis_list'),
    path('thesis/<int:topic_number>/', views.thesis_details, name= 'thesis_details'),    
    path('aboutus/', views.about_us, name= 'about_us'),
    path('thesis/create/', views.create_data, name='create_data'),
    path('thesis/modify/<int:topic_number>/', views.modify_or_delete, name='modify'),
    path('thesis/modify/', views.modify_or_delete, name='modify'),
    path('thesis/delete/<int:topic_number>/', views.modify_or_delete, name='delete_data'),
    path('thesis/delete/', views.modify_or_delete, name='delete_data'),
    path("thesis/review/request/<str:request_type>/<int:topic_number>", views.review_request, name="review_request"),
    path("thesis/review/request", views.review_request, name="review_request"),
    path('settings/<str:account_type>/', views.admin_settings, name='CRUD'),
    path('login/', user_views.login_user, name='login'),
    path('logout/', user_views.logout_user, name='logout'),
    path("thesis/request/<str:crud_action>/", views.request_crud, name="create_request"),
    path("thesis/request/<str:crud_action>/<int:topic_number>", views.request_crud, name="create_request"),
    path("thesis/request/<str:crud_action>/<str:status>/", views.request_crud, name="create_request"),
    path("thesis/request/<str:crud_action>/<str:status>/<int:topic_number>/", views.request_crud, name="create_request"),
    
    # path('test/', views.data_retrieval_test), # for troubleshooting purposes
    # path('add_prev_data/', views.add_previous_data), # add previous given data
    # path('create_user/', user_views.create_new_user), # create users for testing
    # path('create_user/add_permission/', user_views.add_permissions)
]

handler404 = 'main.views.handling_404'
