from django.urls import path
from .views import *

urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('catalog/<slug>/', CatalogView.as_view(), name='catalog_filter'),
    path('course_detail/<pk>/', CourseDetail.as_view(), name='course_detail'),
    path('module_detail/<pk>/', ModuleDetail.as_view(), name='module_detail'),
    path('content_detail/<pk>/', OwnerContentDetail.as_view(), name='content_detail'),
    path('enroll-course/', StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    path('unenroll-course/', StudentUnEnrollCourseView.as_view(), name='student_unenroll_course'),
    
    path('myeducation/', CourseRegistred.as_view(), name='my_edu'),
    path('myeducation/<slug>', CourseRegistred.as_view(), name='my_edu_filer'),
]