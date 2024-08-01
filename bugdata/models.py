from django.db import models

# Create your models here.

class BugList(models.Model):
    btitle = models.CharField(max_length = 100)
    project = models.CharField(max_length = 100)
    btype = models.CharField(max_length = 100)
    tech = models.CharField(max_length = 100)
    bstatus = models.CharField(max_length = 100)
    approve = models.BooleanField(default=False)
    bdescription = models.TextField()


class SolutionList(models.Model):
	bug = models.OneToOneField(
		BugList,
		on_delete = models.CASCADE,
		)
	solution = models.TextField()
