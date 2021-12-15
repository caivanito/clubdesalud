from django.urls import path, include

from app.views.professional.views import *
from app.views.specialty.views import *
from app.views.pathology.views import *
from app.views.patient.views import *
from app.views.medicalbackground.views import *

app_name = 'app'

urlpatterns = [
    # index
    path('', IndexView.as_view(), name='index'),
    # professional
    path('professional/list/', ProfessionalListView.as_view(), name='professional_list'),
    path('professional/add/', ProfessionalCreateView.as_view(), name='professional_create'),
    path('professional/update/<int:pk>/', ProfessionalUpdateView.as_view(), name='professional_update'),
    path('professional/delete/<int:pk>/', ProfessionalDeleteView.as_view(), name='professional_delete'),
    # specialty
    path('specialty/list/', SpecialtyListView.as_view(), name='specialty_list'),
    path('specialty/add/', SpecialtyCreateView.as_view(), name='specialty_create'),
    # pathology
    path('pathology/list/', PathologyListView.as_view(), name='pathology_list'),
    path('pathology/add/', PathologyCreateView.as_view(), name='pathology_create'),
    # patient
    path('patient/list/', PatientListView.as_view(), name='patient_list'),
    path('patient/add/', PatientCreateView.as_view(), name='patient_create'),
    path('patient/delete/<int:pk>/', PatientDeleteView.as_view(), name='patient_delete'),
    path('patient/update/<int:pk>/', PatientUpdateView.as_view(), name='patient_update'),
    # MedicalBackground
    path('patient/listmb/<int:pk>/', MedicalBackgroundListView.as_view(), name='listMedicalBackground'),
    path('patient/addmb/<int:pk>/', MedicalBackgroundCreateView.as_view(), name='addMedicalBackground'),
    path('patient/updatemb/<int:pk>/', MedicalBackgroundUpdateView.as_view(), name='updateMedicalBackground'),

    # path('patient/addMedicalBackground/', addMedicalBackground, name='addMedicalBackground'),

]
