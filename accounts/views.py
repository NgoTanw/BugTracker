from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import auth,messages
from accounts.models import User
from django.contrib.auth import password_validation
from django.core.mail import send_mail
from project.models import ProjectList
from bugdata.models import BugList, SolutionList
import math
import random
from django.conf import settings
from django.core.files.storage import FileSystemStorage

otp = None
flag = 0
# Create your views here.

def about(request):
	return render(request, 'about.html')

def contact(request):
	return render(request, 'contactus.html')

def home(request):
	global flag
	userdata = User.objects.all()
	if flag==1:
		if not request.user.is_authenticated:
			return render(request, 'index.html')
		elif request.user.is_superuser:
			projectdata = ProjectList.objects.all()
			return render(request, 'admin/adminhome.html', {'projects' : projectdata})
		elif request.user.is_staff:
			bugs = BugList.objects.all()
			solutions=SolutionList.objects.all()
			return render(request, 'dev/devhome.html', {'bugs' : bugs, 'userdata':userdata, 'solutions':solutions})
		else:
			bugs = BugList.objects.all()
			solutions=SolutionList.objects.all()
			return render(request, 'tester/testerhome.html', {'bugs' : bugs, 'solutions':solutions})
	elif flag==0:
		auth.logout(request)
		return render(request, 'index.html')


def tester(request):
	if request.user.is_authenticated:
		return redirect('home')

	if request.method=="POST":
		username=request.POST['username']
		password=request.POST['password']

		user=auth.authenticate(username=username,password=password)

		if user is not None:
			if not user.is_superuser:
				if not user.is_staff:
					auth.login(request,user)
					return redirect('otpVerify')
				else:
					messages.warning(request,'invalid credentials')
					return redirect('tester')
			else:
				messages.warning(request,'invalid credentials')
				return redirect('tester')
		else:
			messages.warning(request,'invalid credentials')
			return redirect('tester')
	else:
		return render(request,'tester/testerlogin.html')

def admin(request):
	if request.user.is_authenticated:
		return redirect('home')

	if request.method=="POST":
		username=request.POST['username']
		password=request.POST['password']

		user=auth.authenticate(username=username,password=password)

		if user is not None:
			if user.is_superuser:
				auth.login(request,user)
				return redirect('otpVerify')
			else:
				messages.warning(request,'invalid credentials')
				return redirect('admin')
		else:
			messages.warning(request,'invalid credentials')
			return redirect('admin')
	else:
		return render(request,'admin/adminlogin.html')

def dev(request):
	if request.user.is_authenticated:
		return redirect('home')

	if request.method=="POST":
		username=request.POST['username']
		password=request.POST['password']

		user=auth.authenticate(username=username,password=password)

		if user is not None:
			if not user.is_superuser:
				if user.is_staff:
					auth.login(request,user)
					return redirect('otpVerify')
				else:
					messages.warning(request,'invalid credentials')
					return redirect('dev')
			else:
				messages.warning(request,'invalid credentials')
				return redirect('dev')
		else:
			messages.warning(request,'invalid credentials')
			return redirect('dev')
	else:
		return render(request,'dev/devlogin.html')


def otpGen(request):
	string = '0123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ'
	OTP = ''
	for i in range(6):
		OTP += string[math.floor(random.random() * len(string))]
	return OTP

def otpSend(request,user,otp):
    emailto = user.email
    if emailto:
    	send_mail(
			"OTP",
			"Your OTP is "+otp+". Do not share it with anyone by any means. This is confidential and to be used by you only.",
			'admin@no-reply.com',
			[emailto],
			fail_silently=False,
			)

def otpVerify(request):
	global otp
	global flag
	user = request.user
	if otp == None:
		otp = otpGen(request)
		otpSend(request,user,otp)
		return render(request,'otp.html')
	else:
		if request.method == "POST":
			otpfield = request.POST['otp']
			if otpfield == otp:
				flag=1
				return redirect('home')
			else:
				auth.logout(request)
				return redirect('home')
		else:
			otp = otpGen(request)
			otpSend(request,user,otp)
			auth.logout(request)
			return render(request,'otp.html')

def signup(request):
	if request.method=='POST':
		email=request.POST['email']
		username=request.POST['username']
		usertype=request.POST['usertype']
		password1=request.POST['password1']
		password2=request.POST['password2']

		if password1==password2:
			if User.objects.filter(username=username).exists():
				messages.warning(request,'Username Taken')
				return redirect('signup')
			elif User.objects.filter(email=email).exists():
				messages.warning(request,'Email already exists')
			else:
				user=User.objects.create_user(username=username,password=password1,email=email)
				if usertype=="dev":
					user.is_staff = True
				user.save();
				messages.warning(request,"Account Created Successfully")
				return redirect('home')
		else:
			messages.warning(request,"Password doesn't match")
		return redirect('/')
	else:
		return render(request,'signup.html')


def logout(request):
	global flag
	flag=0
	auth.logout(request)
	return redirect('home')

def resetPassword(request):
	if request.method=="POST":
		email=request.POST['email']
		password1=request.POST['password1']
		password2=request.POST['password2']
		if User.objects.filter(email=email).exists():
			user = User.objects.get(email=email)
			user.set_password(password1)
			user.save()
			return redirect('home')
		else:
			messages.warning(request,'Email does not exist')
			return render(request, 'resetPassword')
	else:
		return render(request, 'passwordreset.html')

def changePassword(request):
	user = request.user
	if request.method=="POST":
		password1=request.POST['password1']
		password2=request.POST['password2']
		passwordnow=request.POST['passwordnow']
		if password1==password2:
			if user.check_password(passwordnow):
				user.set_password(password1)
				user.save()
				return redirect('devProfile')
			else:
				messages.warning(request,'Password incorrect')
				return redirect('changePassword')
		else:
			messages.warning(request,'Password does not match')
			return redirect('changePassword')
	else:
		return render(request, 'changepassword.html')

def devProfile(request):
	user=request.user
	if request.method == 'POST' and 'upload_photo' in request.POST:
		if request.FILES['pic']:
			image = request.FILES['pic']
			fs = FileSystemStorage()
			imagename = fs.save(image.name, image)
			pic = fs.url(imagename)
			if pic is not None:
				user.pic=pic
			user.save()
	if request.method == 'POST' and 'update' in request.POST:
		user.email=request.POST['email']
		first_name=request.POST['first_name']
		last_name=request.POST['last_name']
		gender=request.POST['gender']
		mobile=request.POST['mobile']
		if first_name is not None and last_name is not None:
			user.first_name=first_name
			user.last_name=last_name
		if gender is not None and not gender == "":
			user.gender=gender
		if mobile is not None:
			user.mobile=mobile
		user.save()
	return render(request,'dev/devprofile.html',{'user':user})

def testerProfile(request):
	user=request.user
	if request.method == 'POST' and 'upload_photo' in request.POST:
		if request.FILES['pic']:
			image = request.FILES['pic']
			fs = FileSystemStorage()
			imagename = fs.save(image.name, image)
			pic = fs.url(imagename)
			if pic is not None:
				user.pic=pic
			user.save()
	if request.method == 'POST' and 'update' in request.POST:
		user.email=request.POST['email']
		first_name=request.POST['first_name']
		last_name=request.POST['last_name']
		gender=request.POST['gender']
		mobile=request.POST['mobile']
		if first_name is not None and last_name is not None:
			user.first_name=first_name
			user.last_name=last_name
		if gender is not None and not gender == "":
			user.gender=gender
		if mobile is not None:
			user.mobile=mobile
		user.save()
	return render(request,'tester/testerprofile.html',{'user':user})

def manageUser(request):
	userdata=User.objects.all()
	return render(request,'admin/manageuser.html',{'userdata':userdata})

def editUser(request,id):
	userdata = User.objects.get(id=id)
	if request.method == 'POST':
		userdata.email=request.POST['email']
		name=request.POST['name']
		gender=request.POST['gender']
		mobile=request.POST['mobile']
		dob=request.POST['dob']
		if name is not None and not name=="":
			userdata.name=name
		if gender is not None and not gender=="":
			userdata.gender=gender
		if mobile is not None and not mobile=="":
			userdata.mobile=mobile
		if not dob == "" and dob is not None:
			userdata.dob=dob
		userdata.save()
	return render(request,'admin/edituser.html',{'userdata':userdata})

def deleteUser(request,id):
	userdata = User.objects.get(id=id)
	userdata.delete()
	return render(request, 'manageUser')
