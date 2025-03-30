from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from .models import *
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template.defaultfilters import slugify
from django.http import Http404
from django.views.generic.base import View, TemplateResponseMixin
from django.contrib.postgres.search import SearchVector
from .forms import SearchForm

class PermisionCheckMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.groups.filter(name='Instructors').exists():
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
    

class OwnerCourseList(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/instructor/courselist.html'

    def get(self, request, slug=None):
        subjects_list = Subject.objects.all()
        courses = self.model.objects.filter(owner=request.user)
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


class MainPage(ListView):
    model = Course
    template_name = 'courses/main.html'

class CourseOwnerEditMixin(OwnerMixin,PermisionCheckMixin):
    model = Course
    fields = ['title','subject','description','photo','price']
    success_url = reverse_lazy('owner_courses')
    template_name = 'courses/instructor/course_form.html'

    def form_valid(self,form):
        form.instance.owner = self.request.user
        
        return super().form_valid(form)
    
class OwnerCourseCreate(CourseOwnerEditMixin, CreateView):
    pass

class OwnerCourseUpdate(CourseOwnerEditMixin, UpdateView):
    pass


class OwnerCourseDetele(PermisionCheckMixin,DeleteView):
    template_name = 'courses/instructor/course_delete.html'
    model = Course
    success_url = reverse_lazy('owner_courses')

class OwnerCourseModulesList(TemplateResponseMixin, View):
    template_name = 'courses/instructor/modules/module_list.html'
    model = Module
    def get(self, request, pk):
        modules = Module.objects.filter(course__id=pk)
        
        return self.render_to_response({"modules": modules, 'course': Course.objects.get(id=pk)})

class OwnerCourseModuleEdit(PermisionCheckMixin):
    model = Module
    fields = ['title', 'description']
    template_name = 'courses/instructor/modules/new_module.html'

class OwnerCourseModuleCreate(OwnerCourseModuleEdit,CreateView):
    def form_valid(self, form):
       pk = self.kwargs['pk']
       form.instance.slug = slugify(form.instance.title)
       self.success_url = reverse_lazy('course_module_list', kwargs={'pk':pk})
       form.instance.course = Course.objects.get(id=pk)
       
       return super().form_valid(form)
    
class OwnerCourseModuleUpdate(OwnerCourseModuleEdit,UpdateView):
    def form_valid(self, form):
        pk = self.kwargs['module_id']
        self.success_url = reverse_lazy('course_module_list', kwargs={'pk':pk})
        form.instance.course = Course.objects.get(id=pk)
        
        return super().form_valid(form)
    
class OwnerCourseModuleDelete(PermisionCheckMixin,DeleteView):
    template_name = 'courses/instructor/modules/module_delete.html'
    model = Module
    def get_success_url(self):
        return reverse_lazy('course_module_list', kwargs={'pk': self.kwargs['course_id']})
    
class OwnerCourseModuleDetail(DetailView):
    model = Module
    template_name = 'courses/instructor/modules/module_detail.html'

class OwnerContentEdit(PermisionCheckMixin):
    model = Content
    fields = ['title','video_url','description']
    template_name = 'courses/instructor/contents/content_form.html'

class OwnerContentCreate(OwnerContentEdit,CreateView):
    def form_valid(self,form):
        course_id = self.kwargs['course_id']
        module_id = self.kwargs['module_id']
        
        self.success_url = reverse_lazy('course_module_list', kwargs={'pk': course_id})
        form.instance.module = Module.objects.get(id=module_id)

        return super().form_valid(form)
    
class OwnerContentUpdate(OwnerContentEdit, UpdateView):
    def form_valid(self, form):
        course_id = self.kwargs['course_id']
        self.success_url = reverse_lazy('course_module_list', kwargs={'pk': course_id})
        return super().form_valid(form)
    

class OwnerContentDetail(DetailView):
    model = Content
    template_name = 'courses/instructor/contents/content_detail.html'


class OwnerContentDelete(PermisionCheckMixin, DeleteView):
    model = Content
    template_name = 'courses/instructor/contents/content_delete.html'
    def get_success_url(self):
        return reverse_lazy('course_module_list', kwargs={'pk':self.kwargs['course_id']})