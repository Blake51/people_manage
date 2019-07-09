"""people_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PeopleList, name = '人员信息'),
    path('PeopleAdd/', views.PeopleAdd, name = '添加人员'),
    path('MultiPeopleAdd/', views.MultiPeopleAdd, name = '批量导入'),
    path('PeopleEdit/', views.PeopleEdit, name = '修改人员'),
    path('PersonEdit/', views.PersonEdit, name = '修改人员信息'),
    path('PeopleDelete/', views.PeopleDelete, name = '删除人员'),
]
