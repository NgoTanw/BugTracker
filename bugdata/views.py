from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from accounts.models import User
from .models import BugList, SolutionList
from project.models import ProjectList

# Create your views here.

def report(request):
	projects = ProjectList.objects.all()
	if request.method=='POST':
		btitle=request.POST['btitle']
		project=request.POST['project']
		btype=request.POST['btype']
		tech=request.POST['tech']
		bdescription=request.POST['bugdescription']
		if BugList.objects.filter(btitle=btitle).exists() and BugList.objects.filter(project=project).exists() and BugList.objects.filter(tech=tech).exists() and ProjectList.objects.filter(btype=btype).exists():
			messages.info(request,'Bug already in database')
		else:
			bugs = BugList.objects.create(btitle=btitle,btype=btype,project=project,tech=tech,approve=False,bdescription=bdescription)
			bugs.save()
		return redirect('report')
	else:
		return render(request,'tester/testerreport.html',{'projects':projects})

def track(request):
	bugs=BugList.objects.all()
	return render(request,'dev/tracker.html',{'bugs' : bugs})

def bugDetails(request,id):
	user = request.user
	bugs=BugList.objects.get(id=id)
	solutions=SolutionList.objects.filter(bug_id=id)
	if user.is_staff:
		return render(request,'dev/bugdetails.html',{'bugs' : bugs, 'solutions':solutions})
	else:
		return render(request,'tester/bugdetails.html',{'bugs' : bugs, 'solutions':solutions})

def manageBug(request):
	projects = ProjectList.objects.all()
	bugs=BugList.objects.all()
	solutions=SolutionList.objects.all()
	return render(request,'admin/managebug.html',{'bugs' : bugs, 'projects':projects, 'solutions':solutions})

def reportReq(request):
	bugs=BugList.objects.all()
	return render(request,'admin/reportreq.html',{'bugs' : bugs})

def approveBug(request,id):
	bug = BugList.objects.get(id=id)
	bug.approve = True
	bug.save()
	return redirect('reportReq')

def deleteBug(request,id):
	bug = BugList.objects.get(id=id)
	bug.delete()
	return redirect('manageBug')

def editBug(request,id):
	projects = ProjectList.objects.all()
	bugdata = BugList.objects.get(id=id)
	if request.method=='POST':
		bugdata.btitle=request.POST['btitle']
		bugdata.project=request.POST['project']
		bugdata.btype=request.POST['btype']
		bugdata.tech=request.POST['tech']
		bugdata.bdescription=request.POST['bugdescription']
		bugdata.bstatus=request.POST['bstatus']
		bugdata.save()
		return redirect('manageBug')
	else:
		return render(request,'admin/editbug.html',{'projects':projects, 'bugs':bugdata})

def saveSolutions(request,id):
	bugs=BugList.objects.get(id=id)
	if request.method=='POST':
		solution = request.POST['solution']
		bug_id = id
		solutions = SolutionList.objects.create(bug=bugs,bug_id=bug_id,solution=solution)
		solutions.save()
		return redirect('track')
	else:
		return render(request,'dev/addsolution.html',{'bugs' : bugs})

def listSolutions(request,id):
	user = request.user
	bugs = BugList.objects.get(id=id)
	solutions = SolutionList.objects.filter(bug_id=id)
	if user.is_superuser:
		return render(request, 'admin/solutionlist.html',{'solutions':solutions,'bugs':bugs})
	elif user.is_staff:
		return render(request, 'dev/solutionlist.html',{'solutions':solutions,'bugs':bugs})
	else:
		return render(request, 'tester/solutionlist.html',{'solutions':solutions,'bugs':bugs})

def viewSolution(request,id):
	user = request.user
	solutions=SolutionList.objects.get(id=id)
	bugs = solutions.bug
	if user.is_superuser:
		return render(request, 'admin/solution.html',{'solutions':solutions,'bugs':bugs})
	elif user.is_staff:
		return render(request, 'dev/solution.html',{'solutions':solutions,'bugs':bugs})
	else:
		return render(request, 'tester/solution.html',{'solutions':solutions,'bugs':bugs})

def deleteSolution(request,id):
	solutions = SolutionList.objects.get(id=id)
	return redirect('listSolutions')