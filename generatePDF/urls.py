from django.urls import path
from .views import generatePDF

urlpatterns = [
    # path('', generatePDF.as_view(), name = 'generatePDF'),
    path('<int:order_id>/', generatePDF, name = 'generatePDF'),

]