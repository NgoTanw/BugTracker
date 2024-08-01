from django.urls import path
from . import views

urlpatterns = [
	path('newproject',views.addProject, name="addProject"),
	path('editproject/projectId=<int:id>',views.editProject, name="editProject"),
	path('deleteproject/<int:id>',views.deleteProject, name="deleteProject"),
]
