from django.contrib import admin
from .models import *

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title','slug')

class ModuleInline(admin.StackedInline):
    model = Module
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title','owner','subject','description','photo','price','slug','students')
    inlines = [ModuleInline]