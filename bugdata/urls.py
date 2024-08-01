from django.urls import path
from . import views

urlpatterns = [
	path('report/',views.report, name="report"),
	path('bugtracker/',views.track, name="track"),
	path('bugdetails/bugId=<int:id>',views.bugDetails, name="bugDetails"),
	path('managebug/',views.manageBug, name="manageBug"),
	path('reportrequests/',views.reportReq, name="reportReq"),
	path('editbug/bugId=<int:id>',views.editBug, name="editBug"),
	path('approvebug/<int:id>',views.approveBug, name="approveBug"),
	path('deletebug/<int:id>',views.deleteBug, name="deleteBug"),
	path('addsolution/bugId=<int:id>',views.saveSolutions, name="saveSolutions"),
	path('solutionlist/bugId=<int:id>',views.listSolutions, name="listSolutions"),
	path('solution/bugId=<int:id>',views.viewSolution, name="viewSolution"),
	path('deletesolution/<int:id>',views.deleteSolution, name="deleteSolution"),
]
