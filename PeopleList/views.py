from django.shortcuts import render, redirect
from .models import People
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


navlists = ['人员信息']
#主页
def home(request):
	return render(request, 'home.html', {'navlists':navlists})

#人员信息列表
@login_required
def PeopleList(request):
    if request.user.username == 'admin':
        peoplelists = People.objects.all()
    else:
        peoplelists = People.objects.filter(manager = request.user)
    return render(request, 'PeopleList.html', {'navlists':navlists, 'PeopleLists':peoplelists})

#添加人员
@login_required
def PeopleAdd(request):
    if request.method == 'GET':
        return render(request, 'PeopleAdd.html', {'navlists':navlists})
    elif request.method == 'POST':
        name = request.POST['姓名']
        pid = request.POST['证件号']
        department = request.POST['部门']
        classification = request.POST['类别']
        rank = request.POST['职级']
        tel = request.POST['电话']#需要限制
        canteen = request.POST['食堂']  
        try:
            people = People()
            people.name = name
            people.pid = pid
            people.department = department
            people.classification = classification
            people.rank = rank
            people.tel = tel
            people.canteen = canteen
            people.manager =  request.user
            people.pub_date = timezone.datetime.now()
            people.save()
            return redirect('人员信息')
        except Exception as err:
            return render(request, 'PeopleAdd.html', {'错误': '请重新输入!', 'navlists':navlists})
 