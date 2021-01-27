from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Directory(models.Model):
	name = models.CharField(max_length=256)
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) 
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.name}'

class Document(models.Model):
	uploaded_to = models.ForeignKey(Directory, on_delete=models.CASCADE)
	file = models.FileField()
	uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) 
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.file}--{self.uploaded_to.name}'
