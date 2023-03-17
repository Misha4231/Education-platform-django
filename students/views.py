from django.shortcuts import render
from courses.models import *
from courses.views import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import CourseEnrollFrom
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


class CatalogView(TemplateResponseMixin, View):
    model = Course
    template_name = 'students/catalog.html'

    def get(self, request, slug=None):
        subjects_list = Subject.objects.all()
        courses = self.model.objects.all()
        form = SearchForm()
        query = None
        if slug:
            subject = subjects_list.get(slug=slug)
            courses = courses.filter(subject=subject)
        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                courses = self.model.objects.annotate(search=SearchVector('title', 'subject','description'),).filter(search=query)
        
        return self.render_to_response({'subjects_list': subjects_list, 'courses':courses,'form':form, "query":query})
    
class CourseDetail(TemplateResponseMixin, View):
    template_name = 'students/course_detail.html'
    model = Module
    def get(self, request, pk):
        modules = Module.objects.filter(course__id=pk)
        enroll_form = CourseEnrollFrom(initial={'course':Course.objects.get(id=pk)})
        return self.render_to_response({"modules": modules,'enroll_form':enroll_form, 'course': Course.objects.get(id=pk)})
    
class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollFrom
    
    def form_valid(self, form):   
        self.course = form.cleaned_data['course']
        self.success_url = reverse_lazy('my_edu')
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView, self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('my_edu')

class StudentUnEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollFrom
    
    def form_valid(self, form):   
        self.course = form.cleaned_data['course']
        self.success_url = reverse_lazy('my_edu')
        self.course.students.remove(self.request.user)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('my_edu')

class ModuleDetail(DetailView):
    model = Module
    template_name = 'students/module_detail.html'

class OwnerContentDetail(DetailView):
    model = Content
    template_name = 'students/content_detail.html'

class CourseRegistred(TemplateResponseMixin, View):
    model = Course
    template_name = 'students/catalog_r.html'

    def get(self, request, slug=None):
        subjects_list = Subject.objects.all()
        courses = self.model.objects.filter(students=request.user)
        form = SearchForm()
        query = None
        if slug:
            subject = subjects_list.get(slug=slug)
            courses = courses.filter(subject=subject)
        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                courses = self.model.objects.annotate(search=SearchVector('title', 'subject','description'),).filter(search=query)
        
        return self.render_to_response({'subjects_list': subjects_list, 'courses':courses,'form':form, "query":query})

class RegistrationView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'students/register.html'
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],password=cd['password1'])
        login(self.request, user)
        return result