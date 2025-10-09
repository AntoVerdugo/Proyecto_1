from django.db import models

# Create your models here.
class Project(models.Model):  #Creacion de tabla llamada Project
    name =models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Task(models.Model):
    title= models.CharField(max_length=200)
    descipcion = models.TextField()
    project= models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + '-' + self.project.name

