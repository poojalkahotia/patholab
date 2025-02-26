from django.contrib.auth.decorators import login_required
from django.urls import path
from pathoapp import views
from .views import (
    generate_haematology_report, generate_bloodsugar_report, generate_kidney_report,
    generate_urine_report, generate_hiv_report, generate_microalbumin_report,
    ForgotPasswordView, ResetPasswordView, get_next_test_id,home
)
from django.contrib.auth import views as auth_views
#from .reports.haematology_report import generate_haematology_report  # Import the view function
#from .reports.bloodsugar_report import generate_bloodsugar_report  # Import the view

urlpatterns = [
     # Core Pages
     # Home page as the root URL
    path('', views.home, name='home'),  # Alternative home URL
    path('signup/', views.signup, name='signup'),
    path('about/', views.About, name='about'),  # About page
    path('contact/', views.Contact, name='contact'),  # Contact page
    
    # Authentication URLs
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', views.password_change, name='password_change'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset_password'),

   # Doctor Management
    path('adddoctor/', views.adddoctor, name='adddoctor'),
    path('delete/<str:doctorname>/', views.deletedoctor, name='deletedata'),
    path('get-doctor-email/', views.get_doctor_email, name='get_doctor_email'),
    path('doctor_st/', views.doctor_st, name='doctor_st'),

    # Patient Management
    path('addpathoinfo/', views.addpathoinfo, name='addpathoinfo'),
    path('addpatient/', views.addpatient, name='addpatient'),
    path('get_patient_data/', views.get_patient_data, name='get_patient_data'),
    path('viewpatient/', views.viewpatient, name='viewpatient'),
    path('deletepatient/<int:patientid>/', views.deletepatient, name='deletepatient'),
    path('updatepatient/<int:patientid>/', views.updatepatient, name='updatepatient'),

    # Test Management
    path('addhaematology/', views.addhaematology, name='addhaematology'),
    path('viewhaematology/', views.viewhaematology, name='viewhaematology'),
    path('updatehaematology/<str:test_id>/', views.updatehaematology, name='updatehaematology'),
    path('deletehaematology/<str:test_id>/', views.deletehaematology, name='deletehaematology'),
    path('haematology_report/<int:test_id>/', views.generate_haematology_report, name='haematology_report'),

    path('addurine/', views.addurine, name='addurine'),
    path('viewurine/', views.viewurine, name='viewurine'),
    path('updateurine/<str:test_id>/', views.updateurine, name='updateurine'),
    path('deleteurine/<str:test_id>/', views.deleteurine, name='deleteurine'),
    path('urine_report/<int:test_id>/', views.generate_urine_report, name='urine_report'),

    path('addbloodsugar/', views.addbloodsugar, name='addbloodsugar'),
    path('viewbloodsugar/', views.viewbloodsugar, name='viewbloodsugar'),
    path('updatebloodsugar/<str:test_id>/', views.updatebloodsugar, name='updatebloodsugar'),
    path('deletebloodsugar/<str:test_id>/', views.deletebloodsugar, name='deletebloodsugar'),
    path('bloodsugar_report/<int:test_id>/', views.generate_bloodsugar_report, name='bloodsugar_report'),

    path('addkidney/', views.addkidney, name='addkidney'),
    path('viewkidney/', views.viewkidney, name='viewkidney'),
    path('updatekidney/<str:test_id>/', views.updatekidney, name='updatekidney'),
    path('deletekidney/<str:test_id>/', views.deletekidney, name='deletekidney'),
    path('kidney_report/<int:test_id>/', views.generate_kidney_report, name='kidney_report'),

    path('addhiv/', views.addhiv, name='addhiv'),
    path('viewhiv/', views.viewhiv, name='viewhiv'),
    path('updatehiv/<str:test_id>/', views.updatehiv, name='updatehiv'),
    path('deletehiv/<str:test_id>/', views.deletehiv, name='deletehiv'),
    path('hiv_report/<int:test_id>/', views.generate_hiv_report, name='hiv_report'),

    path('addmicroalbumin/', views.addmicroalbumin, name='addmicroalbumin'),
    path('viewmicroalbumin/', views.viewmicroalbumin, name='viewmicroalbumin'),
    path('updatemicroalbumin/<str:test_id>/', views.updatemicroalbumin, name='updatemicroalbumin'),
    path('deletemicroalbumin/<str:test_id>/', views.deletemicroalbumin, name='deletemicroalbumin'),
    path('microalbumin_report/<int:test_id>/', views.generate_microalbumin_report, name='microalbumin_report'),

    # Miscellaneous
    path('getnexttestid/<str:model_name>/', get_next_test_id, name='get_next_test_id'),
    path('daily_report/', views.daily_report, name='daily_report'),
]