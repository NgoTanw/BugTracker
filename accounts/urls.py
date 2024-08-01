from django.urls import path
from . import views

urlpatterns = [
	path('',views.home, name="home"),
	path('signup/',views.signup, name="signup"),
	path('admin/', views.admin, name="admin"),
	path('dev/', views.dev, name="dev"),
	path('tester/', views.tester, name="tester"),
	path('otp/',views.otpVerify, name="otpVerify"),
	path('resetpassword/',views.resetPassword, name="resetPassword"),
	path('changepassword/',views.changePassword, name="changePassword"),
	path('devprofile/',views.devProfile, name="devProfile"),
	path('testerprofile/',views.testerProfile, name="testerProfile"),
	path('manageuser/',views.manageUser, name="manageUser"),
	path('edituser/uuid=<int:id>',views.editUser, name="editUser"),
	path('deleteuser/<int:id>',views.deleteUser, name="deleteUser"),
	path('about/',views.about, name="about"),
	path('contact/',views.contact, name="contact"),
]
