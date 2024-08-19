from django.urls import path
from .views import *

urlpatterns = [
    path('/create/', create_project, name='create_project'),
    path('/get/', get_projects, name='get_projects'),
    path('/delete/<int:id>/', delete_project, name='delete_project'),
    path('/update/<int:id>/', update_project, name='update_project'),
]