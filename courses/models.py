from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title
    
    

class Course(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_owner')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    subject = models.ForeignKey(Subject, related_name='courses_subject', on_delete=models.CASCADE)
    description = models.TextField()
    photo = models.ImageField(upload_to='course/')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    price = models.CharField(max_length=50)
    students = models.ManyToManyField(User, related_name='course_joined', blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return self.title
    
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses_modules')
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['id']
        get_latest_by = ['id']

    def __str__(self) -> str:
        return self.title
    
class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.title