from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import ProjectList
from accounts.models import User

# Create your views here.

def addProject(request):
	userdata = User.objects.all()
	if request.method=='POST':
		ptitle=request.POST['ptitle']
		ptype=request.POST['ptype']
		manager=request.POST['manager']
		frontend=request.POST['frontend']
		backend=request.POST['backend']
		client=request.POST['client']
		pstatus=request.POST['pstatus']
		startdate=request.POST['startdate']
		pdescription=request.POST['pdescription']
		if ProjectList.objects.filter(ptitle=ptitle).exists() and ProjectList.objects.filter(frontend=frontend).exists() and ProjectList.objects.filter(backend=backend).exists() and ProjectList.objects.filter(client=client).exists() and ProjectList.objects.filter(startdate=startdate).exists():
			messages.info(request,'Project already exists')
		else:
			pdata = ProjectList.objects.create(ptitle=ptitle,ptype=ptype,manager=manager,frontend=frontend,backend=backend,client=client,startdate=startdate,pstatus=pstatus,pdescription=pdescription)
			pdata.save()
		return redirect('addProject')
	else:
		return render(request,'admin/addproject.html',{'userdata':userdata})

def editProject(request,id):
	userdata = User.objects.all()
	projectdata = ProjectList.objects.get(id=id)
	if request.method=='POST':
		projectdata.ptitle=request.POST['ptitle']
		projectdata.ptype=request.POST['ptype']
		projectdata.manager=request.POST['manager']
		projectdata.frontend=request.POST['frontend']
		projectdata.backend=request.POST['backend']
		projectdata.client=request.POST['client']
		projectdata.pstatus=request.POST['pstatus']
		projectdata.startdate=request.POST['startdate']
		projectdata.pdescription=request.POST['pdescription']
		projectdata.save()
	return render(request, 'admin/editproject.html', {'projects' : projectdata , 'userdata':userdata})

def deleteProject(request,id):
	project = ProjectList.objects.get(id=id)
	project.delete()
	return render('home')