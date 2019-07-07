from django.shortcuts import render
from .models import People

def home(request):
	return render(request, 'home.html')

def PeopleList(request):
	peoplelists = People.objects.all()
	return render(request, 'PeopleList.html', {'PeopleLists':peoplelists})