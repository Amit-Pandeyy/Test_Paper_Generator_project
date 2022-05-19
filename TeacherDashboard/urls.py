from django.urls import path,include
from .views import teacher_dashboard,show_old_paper


urlpatterns = [

        path("teacher_dashboard",teacher_dashboard,name="teacher_dashboard"),
        path("show_old_paper/<int:id>",show_old_paper,name="show_old_paper")
]