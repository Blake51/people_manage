from django.shortcuts import render, redirect
from .models import People
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .functions import MultiAdd

navlists = ['人员信息', '添加人员', '修改人员']
#主页
def home(request):
	return render(request, 'home.html', {'navlists':navlists})

#人员信息列表
@login_required
def PeopleList(request):
    user_name = request.user.username
    if  user_name== 'admin':
        peoplelists = People.objects.all()
    else:
        peoplelists = People.objects.filter(manager = request.user)
    #需要传递的变量字典
    Var = {'navlists':navlists, 'PeopleLists':peoplelists, 'user_name': user_name}
    return render(request, 'PeopleList.html', Var)

#添加人员
@login_required
def PeopleAdd(request):
    user_name = request.user.username
    Var = {'navlists':navlists, 'user_name': user_name}
    if request.method == 'GET':
        return render(request, 'PeopleAdd.html', Var)
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
            Var.update({'错误': '请重新输入!'})
            return render(request, 'PeopleAdd.html', Var)
#批量导入
@login_required
def MultiPeopleAdd(request):
    user_name = request.user.username
    Var = {'navlists':navlists, 'user_name': user_name}
    if request.method == 'GET':
        return render(request, 'MultiPeopleAdd.html', Var)
    elif request.method == 'POST':
        excel = request.FILES.get('批量导入')
        table = MultiAdd(excel).fetch_table()
        for x in range(1,table.nrows):
            #从第二行开始导入
            try:
                people = People()
                people.name = table.row_values(x)[0]
                people.pid = table.row_values(x)[1]
                people.department = table.row_values(x)[2]
                people.classification = table.row_values(x)[3]
                people.rank = table.row_values(x)[4]
                people.canteen = table.row_values(x)[5]
                people.tel = table.row_values(x)[6]
                people.manager =  request.user
                people.pub_date = timezone.datetime.now()
                people.save()
            except Exception as err:
                Var.update({'错误': '请重新输入!'})
                return render(request, 'MultiPeopleAdd.html', Var)
        return redirect('人员信息')

#修改人员
@login_required
def PeopleEdit(request):
    user_name = request.user.username
    if  user_name== 'admin':
        peoplelists = People.objects.all()
    else:
        peoplelists = People.objects.filter(manager = request.user)
    #需要传递的变量字典
    Var = {'navlists':navlists, 'PeopleLists':peoplelists, 'user_name': user_name}
    
    if request.method == 'GET':
        return render(request, 'PeopleEdit.html', Var)
    elif request.method == 'POST':
        #try:
            box_chosen = request.POST.get('选项')
            person = People.objects.get(pk = box_chosen)
            Var.update({'person': person})            
            if 'update' in request.POST:
                return render(request, 'PersonEdit.html', Var) #update功能实现
            elif 'del' in request.POST: 
                return PeopleDelete(request)#del功能实现，带参数重定向至'删除人员'             
            else:
                return render(request, 'PeopleList.html', Var) #异常返回
        #except:
            #return render(request, 'PeopleList.html', Var)

#修改人员信息
@login_required
def PersonEdit(request):
    user_name = request.user.username
    Var = {'navlists':navlists, 'user_name': user_name}
    if request.method == 'GET':
        return render(request, 'PeopleEdit.html', Var)
    elif request.method == 'POST':
        try:
            box_chosen = request.POST.get('选项')
            person = People.objects.get(pk = box_chosen)
            Var.update({'person': person})
            return render(request, 'PersonEdit.html', Var)
        except:
            if 'pk' in request.POST:
            #获取表单内修改信息
                pk = request.POST['pk']
                name = request.POST['姓名']
                pid = request.POST['证件号']
                department = request.POST['部门']
                classification = request.POST['类别']
                rank = request.POST['职级']
                tel = request.POST['电话']#需要限制
                canteen = request.POST['食堂']  
                try:
                    people = People.objects.get(pk = pk)
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
                    Var.update({'错误': '无法获取人员信息'})
                    return render(request, 'PersonEdit.html', Var)                     
            else:
                Var.update({'错误': '表单信息不全'})
                return render(request, 'PersonEdit.html', Var) 

       
#删除人员
@login_required
def PeopleDelete(request):
    user_name = request.user.username
    Var = {'navlists':navlists, 'user_name': user_name}
    if request.method == 'GET':
        return render(request, 'PeopleEdit.html', Var)
    elif request.method == 'POST':
        try:
            persons = []
            box_chooses = request.POST.getlist('选项')
            box_chosens = request.POST.getlist('选中')
            if box_chooses:
                for box_choose in box_chooses:
                    person = People.objects.get(pk = box_choose) 
                    persons.append(person) 
                Var.update({'persons':persons})
                return render(request, 'PeopleDelete.html', Var)# 
            if box_chosens:
                for box_chosen in box_chosens:
                    People.objects.filter(pk = box_chosen).delete()
                return redirect('修改人员')
            return redirect('人员信息')            
        except Exception as err:       
            Var.update({'错误': '出现错误!'})
            return render(request, 'PeopleEdit.html', Var)     

 