from django.urls import path
from .views import *

urlpatterns = [
    path('owner_courses/', OwnerCourseList.as_view(), name='owner_courses'),
    path('owner_courses/<slug>/', OwnerCourseList.as_view(), name='owner_courses_sorted'),
    path('owner_course_create/', OwnerCourseCreate.as_view(), name='course_create'),
    path('owner_course_edit/<pk>/', OwnerCourseUpdate.as_view(), name='course_edit'),
    path('<pk>/owner_course_delete/', OwnerCourseDetele.as_view(), name='course_delete'),
    path('owner_course_module_list/<pk>/', OwnerCourseModulesList.as_view(), name='course_module_list'),
    path('owner_course_module_create/<pk>/', OwnerCourseModuleCreate.as_view(), name='course_module_create'),
    path('owner_course_module_update/<pk>/<int:module_id>/', OwnerCourseModuleUpdate.as_view(), name='course_module_update'),
    path('owner_course_module_delete/<pk>/<int:course_id>/', OwnerCourseModuleDelete.as_view(), name='course_module_delete'),
    path('owner_course_module_detail/<pk>/', OwnerCourseModuleDetail.as_view(), name='course_module_detail'),
    path('owner_content_create/<int:course_id>/<int:module_id>/', OwnerContentCreate.as_view(), name='course_content_create'),
    path('owner_content_update/<int:course_id>/<pk>/', OwnerContentUpdate.as_view(), name='course_content_update'),
    path('owner_content_detail/<pk>/', OwnerContentDetail.as_view(), name='owner_content_detail'),
    path('owner_content_delete/<pk>/<int:course_id>/', OwnerContentDelete.as_view(), name='owner_content_delete'),
]