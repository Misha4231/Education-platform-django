from django import forms
from courses.models import Course
from django.contrib.auth.models import User

class CourseEnrollFrom(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),widget=forms.HiddenInput)
