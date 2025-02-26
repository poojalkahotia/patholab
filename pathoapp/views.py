# Django Core Imports
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse
from django.contrib import messages
from django.db.models import Q, Max
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.apps import apps
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.http import require_GET
from django.templatetags.static import static

# Models and Forms
from .models import *
from .forms import *
#from .models import Haematology, BloodSugar, Kidney, Urine, HIV, Microalbumin  # ✅ Models को import करें

# Reports Imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from pathoapp.reports.haematology_report import HaematologyReport
from .reports.bloodsugar_report import BloodSugarReport
from .reports.kidney_report import KidneyReport
from .reports.urine_report import UrineReport
from .reports.hiv_report import HivReport
from .reports.microalbumin_report import MicroalbuminReport
from pathoapp.models import Haematology, Pathoinfo 
# Other Utilities
import os
from io import BytesIO

# Authentication Views
class ForgotPasswordView(View):
    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, 'pathoapp/forgot_password.html', {'form': form})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                # Generate token and send email
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = request.build_absolute_uri(
                    reverse('reset_password', kwargs={'uidb64': uid, 'token': token})
                )
                subject = "Password Reset Request"
                message = f"Click the link below to reset your password:\n\n{reset_url}"
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
                messages.success(request, "Password reset link has been sent to your email.")
            else:
                messages.error(request, "No user found with this email address.")
            return redirect('forgot_password')
        return render(request, 'pathoapp/forgot_password.html', {'form': form})

class ResetPasswordView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                form = ResetPasswordForm(user)
                return render(request, 'reset_password.html', {'form': form})
            else:
                messages.error(request, "Invalid or expired token.")
                return redirect('forgot_password')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "Invalid link.")
            return redirect('forgot_password')

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                form = ResetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Your password has been reset successfully.")
                    return redirect('login')
                else:
                    return render(request, 'reset_password.html', {'form': form})
            else:
                messages.error(request, "Invalid or expired token.")
                return redirect('forgot_password')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "Invalid link.")
            return redirect('forgot_password')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'pathoapp/login.html')

@login_required
def password_change(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Check if the old password is correct
        if not request.user.check_password(old_password):
            messages.error(request, 'Your old password was entered incorrectly. Please try again.')
            return redirect('password_change')

        # Check if new passwords match
        if new_password1 != new_password2:
            messages.error(request, 'The new passwords do not match. Please try again.')
            return redirect('password_change')

        # Change the password
        request.user.set_password(new_password1)
        request.user.save()

        # Update session to prevent logout
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Your password has been changed successfully!')
        return redirect('home')

    return render(request, 'pathoapp/change_password.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, 'Account created successfully. Please login.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('pathoapp/signup')
    else:
        return render(request, 'pathoapp/signup.html')
    
# General Views
@login_required(login_url='login')
def home(request):
    haematology_tests = Haematology.objects.all()
    bloodsugar_tests = BloodSugar.objects.all()
    kidney_tests = Kidney.objects.all()
    urine_tests = Urine.objects.all()
    hiv_tests = Hiv.objects.all()
    microalbumin_tests = Microalbumin.objects.all()

    context = {
        'haematology_tests': haematology_tests,
        'bloodsugar_tests': bloodsugar_tests,
        'kidney_tests': kidney_tests,
        'urine_tests': urine_tests,
        'hiv_tests': hiv_tests,
        'microalbumin_tests': microalbumin_tests,
    }
    return render(request, 'pathoapp/home.html', context)

def About(request):
    return render(request, 'pathoapp/about.html')

def Contact(request):
    return render(request, 'pathoapp/contact.html')

def Index(request):
    return render(request, 'pathoapp/index.html')

# Doctor and Patient Views
def adddoctor(request):
    if request.method == 'POST':
        fm = DoctorForm(request.POST)
        if fm.is_valid():
           fm.save()
        messages.add_message(request, messages.SUCCESS, 'Data Saved Successfully !!!')
        fm = DoctorForm() #data save hone ke baad phir se blank form aa jaye isliye
            
    else:
        fm = DoctorForm()
    doctor = Doctor.objects.all()
    return render(request, 'pathoapp/adddoctor.html',{'form':fm, 'doc':doctor})

def deletedoctor(request, doctorname):  # Accept 'doctorname' as a parameter
    if request.method == 'POST':
        Doctor.objects.filter(doctorname=doctorname).delete()  # Filter by doctorname and delete
        messages.add_message(request, messages.SUCCESS, 'Doctor Deleted Successfully !!!')
    return redirect('pathoapp/adddoctor')  # Redirect to 'adddoctor' page after deletion

def get_doctor_email(request):
    doctor_name = request.GET.get('doctorname', None)  # Get doctorname from AJAX request

    if doctor_name:
        try:
            doctor = Doctor.objects.get(doctorname=doctor_name)  # Fetch doctor by name
            return JsonResponse({'email': doctor.email})  # Return email in JSON format
        except Doctor.DoesNotExist:
            return JsonResponse({'email': ''})  # Return empty string if doctor does not exist
    return JsonResponse({'email': ''})

def addpatient(request):
    doctors = Doctor.objects.all()  # Fetch all doctors for dropdown

    if request.method == 'POST':
        patientid = request.POST['patientid']
        patientname = request.POST['patientname']
        age = request.POST['age']
        gender = request.POST['gender']
        mobile = request.POST['mobile']
        email = request.POST['email']
        address = request.POST['address']
        recondate = request.POST['recondate']
        doctor_name = request.POST['refbydoctor']  # Get selected doctor from dropdown

        try:
            # Fetch doctor instance by doctorname (since it's the primary key)
            doctor = Doctor.objects.get(doctorname=doctor_name)

            # Create a new PatientMaster record
            PatientMaster.objects.create(
                patientid=patientid,
                patientname=patientname,
                age=age,
                gender=gender,
                mobile=mobile,
                email=email,
                address=address,
                recondate=recondate,
                refbydoctor=doctor  # Save doctor reference
            )
            messages.success(request, 'Patient added successfully!')
            return redirect('viewpatient')  # Redirect to view patient after saving
        except Doctor.DoesNotExist:
            messages.error(request, 'Selected doctor does not exist.')
            return render(request, 'pathoapp/addpatient.html', {'error': 'yes', 'doctors': doctors})
        except Exception as e:
            messages.error(request, 'Something went wrong, please try again.')
            return render(request, 'pathoapp/addpatient.html', {'error': 'yes', 'doctors': doctors})

    return render(request, 'pathoapp/addpatient.html', {'doctors': doctors, 'error': 'no'})

def viewpatient(request):
    # Fetch all patient records including related doctor details
    patients = PatientMaster.objects.select_related('refbydoctor').all()

    # Pass the patient data to the template
    context = {
        'patients': patients
    }
    return render(request, 'pathoapp/viewpatient.html', context)

def deletepatient(request, patientid):
       # Get the patient object, or return a 404 if not found
    patient_data = get_object_or_404(PatientMaster, patientid=patientid)

    if request.method == 'POST':
        # Delete the patient record
        patient_data.delete()
        messages.success(request, "Record deleted successfully!")
        return redirect('pathoapp/viewpatient')
    return redirect('pathoapp/viewpatient')

def updatepatient(request, patientid):
    # Get the patient instance
    patient = get_object_or_404(PatientMaster, patientid=patientid)
    doctors = Doctor.objects.all()  # Fetch all doctors for dropdown

    if request.method == 'POST':
        # Update patient data from form
        patient.patientname = request.POST['patientname']
        patient.recondate = request.POST['recondate']
        patient.age = request.POST['age']
        patient.gender = request.POST['gender']
        patient.mobile = request.POST['mobile']
        patient.email = request.POST['email']
        patient.address = request.POST['address']
        doctor_name = request.POST['refbydoctor']
        patient.refbydoctor = get_object_or_404(Doctor, doctorname=doctor_name)

        try:
            patient.save()  # Save updated patient information
            messages.success(request, 'Patient updated successfully!')
            return redirect('viewpatient')  # Redirect back to the view patient page
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    # Render the update form with patient and doctor data
    return render(request, 'pathoapp/updatepatient.html', {'patient': patient, 'doctors': doctors})

#test views
def addhaematology(request):
    # Get the next test ID for the Haematology test
    max_test_id = Haematology.objects.aggregate(Max('test_id'))['test_id__max']
    next_test_id = (max_test_id + 1) if max_test_id is not None else 1

    # Fetch all patients from the PatientMaster model
    patients = PatientMaster.objects.all()

    if request.method == 'POST':
        form = HaematologyForm(request.POST)
        if form.is_valid():
            patient_id = request.POST.get('patient_id')  # Get patient_id from the form
            

            try:
                # Fetch the PatientMaster instance using the patient_id
                patient = PatientMaster.objects.get(pk=patient_id)

                # Fetch the Doctor instance using the doctor name
                doctor = patient.refbydoctor  # Get the doctor from the patient's refbydoctor field

                # Create a Haematology instance without saving it yet
                haematology_test = form.save(commit=False)
                haematology_test.test_id = next_test_id
                haematology_test.patient = patient
                haematology_test.doctor = doctor  # Assign the doctor

                # Populate the Haematology instance with data from PatientMaster
                haematology_test.patientname = patient.patientname
                haematology_test.age = patient.age
                haematology_test.gender = patient.gender
                haematology_test.mobile = patient.mobile
                haematology_test.email = patient.email

                # Save the Haematology instance
                haematology_test.save()

                # Update the next_test_id for the form
                next_test_id += 1

                messages.success(request, 'Haematology test added successfully.')
                form = HaematologyForm(initial={'test_id': next_test_id})
                return render(request, 'pathoapp/addhaematology.html', {'form': form, 'next_test_id': next_test_id, 'patients': patients})
            except PatientMaster.DoesNotExist:
                messages.error(request, 'Patient ID not found.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    else:
        # For GET requests, initialize the form with the next_test_id
        form = HaematologyForm(initial={'test_id': next_test_id})

    return render(request, 'pathoapp/addhaematology.html', {'form': form, 'next_test_id': next_test_id, 'patients': patients})

def viewhaematology(request):
    # Fetch all Haematology tests from the database
    haematology_tests = Haematology.objects.all()

    # Pass the test data to the template for rendering
    return render(request, 'pathoapp/viewhaematology.html', {
        'haematology_tests': haematology_tests
    })

def updatehaematology(request, test_id):
    # Fetch the Haematology test instance or show a 404 page if not found
    haematology_test = get_object_or_404(Haematology, test_id=test_id)

    if request.method == 'POST':
        # Bind form to POST data
        form = HaematologyForm(request.POST, instance=haematology_test)
        if form.is_valid():
            # Save the updated test if the form is valid
            form.save()
            messages.success(request, 'Data Updated Successfully.')
            return redirect('viewhaematology')
        else:
            # Add form errors to the context for debugging
            messages.error(request, 'Please correct the errors below.')
            print("Form Errors:", form.errors)  # Debugging information
    else:
        # Pre-populate the form with existing instance data
        form = HaematologyForm(instance=haematology_test)

    # Fetch the patient information from the PatientMaster associated with the Haematology test
    patient_data = haematology_test.patient  # Get the associated PatientMaster instance

    # Pre-fill the form with the patient's ID (as this can be changed)
    form.fields['patient_id'].initial = patient_data.patientid  # Assign initial patient ID value
    
    # Fetch additional data (refbydoctor and doctor_email) from PatientMaster
    patient_data.refbydoctor = patient_data.refbydoctor  # Fetch referred doctor name
    patient_data.email = patient_data.email  # Fetch doctor email

    # Render the update form template with the form and patient data
    return render(request, 'pathoapp/updatehaematology.html', {
        'form': form,
        'test_id': test_id,
        'patient_data': patient_data  # Pass the patient data to the template
    })


def deletehaematology(request, test_id):
    # Get the Haematology test record to be deleted
    haematology_test = get_object_or_404(Haematology, test_id=test_id)
    
    # Delete the record
    haematology_test.delete()
    
    # Add a success message
    messages.success(request, 'Haematology test deleted successfully.')
    
    # Redirect to the view page
    return redirect('viewhaematology')

def get_patient_data(request):
    patient_id = request.GET.get('patient_id')
    if patient_id:
        try:
            # Fetch the patient record
            patient = PatientMaster.objects.get(pk=patient_id)
            
            # Fetch the referring doctor's email (if any)
            doctor_email = patient.refbydoctor.email if patient.refbydoctor else None
            
            # Prepare the response data
            data = {
                'patientname': patient.patientname,
                'age': patient.age,
                'gender': patient.gender,
                'mobile': patient.mobile,
                'email': patient.email,  # Patient's email
                'doctorname': patient.refbydoctor.doctorname if patient.refbydoctor else None,
                'doctoremail': doctor_email,  # Referring doctor's email
            }
            return JsonResponse(data)
        except PatientMaster.DoesNotExist:
            return JsonResponse({'error': 'Patient not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

#Yeh file sirf request handling aur response return karne ke liye hogi. 
# Isme haematology_report.py se HaematologyReport class import ki jayegi.
def generate_haematology_report(request, test_id):
    # Fetch the Haematology test
    haematology_test = get_object_or_404(Haematology, test_id=test_id)

    # Fetch pathology info
    pathology_info = Pathoinfo.objects.first()

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="haematology_report_{test_id}.pdf"'

    # Create the report
    report = HaematologyReport(response, haematology_test)
    report.generate(pathology_info)
    return response


        
def addbloodsugar(request):
    # Get the next test ID for the BloodSugar test
    max_test_id = BloodSugar.objects.aggregate(Max('test_id'))['test_id__max']
    next_test_id = (max_test_id + 1) if max_test_id is not None else 1

    # Fetch all patients from the PatientMaster model
    patients = PatientMaster.objects.all()

    if request.method == 'POST':
        form = BloodSugarForm(request.POST)
        if form.is_valid():
            patient_id = request.POST.get('patient_id')  # Get patient_id from the form
            try:
                # Fetch the PatientMaster instance using the patient_id
                patient = PatientMaster.objects.get(pk=patient_id)

                # Fetch the Doctor instance from the patient's refbydoctor field
                doctor = patient.refbydoctor  # Get the doctor from the patient's refbydoctor field

                # Create a BloodSugar instance without saving it yet
                bloodsugar_test = form.save(commit=False)
                bloodsugar_test.test_id = next_test_id
                bloodsugar_test.patient = patient
                bloodsugar_test.doctor = doctor  # Assign the doctor

                # Populate the BloodSugar instance with data from PatientMaster
                bloodsugar_test.patientname = patient.patientname
                bloodsugar_test.age = patient.age
                bloodsugar_test.gender = patient.gender
                bloodsugar_test.mobile = patient.mobile
                bloodsugar_test.email = patient.email

                # Save the BloodSugar instance
                bloodsugar_test.save()

                # Update the next_test_id for the form
                next_test_id += 1

                messages.success(request, 'Blood Sugar test added successfully.')
                form = BloodSugarForm(initial={'test_id': next_test_id})
                return render(request, 'pathoapp/addbloodsugar.html', {'form': form, 'next_test_id': next_test_id, 'patients': patients})
            except PatientMaster.DoesNotExist:
                messages.error(request, 'Patient ID not found.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    else:
        # For GET requests, initialize the form with the next_test_id
        form = BloodSugarForm(initial={'test_id': next_test_id})

    return render(request, 'pathoapp/addbloodsugar.html', {'form': form, 'next_test_id': next_test_id, 'patients': patients})

def viewbloodsugar(request):
    # Fetch all bloodsugar tests from the database
    bloodsugar_tests = BloodSugar.objects.all()

    # Pass the test data to the template for rendering
    return render(request, 'pathoapp/viewbloodsugar.html', {
        'bloodsugar_tests': bloodsugar_tests
    })

def updatebloodsugar(request, test_id):
    # Fetch the bloodsugar test instance or show a 404 page if not found
    bloodsugar_test = get_object_or_404(BloodSugar, test_id=test_id)

    if request.method == 'POST':
        # Bind form to POST data
        form = BloodSugarForm(request.POST, instance=bloodsugar_test)
        if form.is_valid():
            # Save the updated test if the form is valid
            form.save()
            messages.success(request, 'Data Updated Successfully.')
            return redirect('viewbloodsugar')
        else:
            # Add form errors to the context for debugging
            messages.error(request, 'Please correct the errors below.')
            print("Form Errors:", form.errors)  # Debugging information
    else:
        # Pre-populate the form with existing instance data
        form = BloodSugarForm(instance=bloodsugar_test)

    # Fetch the patient information from the PatientMaster associated with the bloodsugar test
    patient_data = bloodsugar_test.patient  # Get the associated PatientMaster instance

    # Pre-fill the form with the patient's ID (as this can be changed)
    form.fields['patient_id'].initial = patient_data.patientid  # Assign initial patient ID value
    
    # Fetch additional data (refbydoctor and doctor_email) from PatientMaster
    patient_data.refbydoctor = patient_data.refbydoctor  # Fetch referred doctor name
    patient_data.email = patient_data.email  # Fetch doctor email

    # Render the update form template with the form and patient data
    return render(request, 'pathoapp/updatebloodsugar.html', {
        'form': form,
        'test_id': test_id,
        'patient_data': patient_data  # Pass the patient data to the template
    })


def deletebloodsugar(request, test_id):
    # Get the bloodsugar test record to be deleted
    bloodsugar_test = get_object_or_404(BloodSugar, test_id=test_id)
    
    # Delete the record
    bloodsugar_test.delete()
    
    # Add a success message
    messages.success(request, 'BloodSugar test deleted successfully.')
    
    # Redirect to the view page
    return redirect('viewbloodsugar')

def generate_bloodsugar_report(request, test_id):
    # Fetch the Blood Sugar test
    bloodsugar_test = get_object_or_404(BloodSugar, test_id=test_id)
    # Fetch pathology info
    pathology_info = Pathoinfo.objects.first()
    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bloodsugar_report_{test_id}.pdf"'
    # Create the report
    report = BloodSugarReport(response, bloodsugar_test)
    report.generate(pathology_info)
    return response

def addkidney(request):
     # Get the next test ID for the Kidney test
    max_test_id = Kidney.objects.aggregate(Max('test_id'))['test_id__max']
    next_test_id = (max_test_id + 1) if max_test_id is not None else 1

    # Fetch all patients from the PatientMaster model
    patients = PatientMaster.objects.all()

    if request.method == 'POST':
        form = KidneyForm(request.POST)
        if form.is_valid():
            patient_id = request.POST.get('patient_id')  # Get patient_id from the form
            try:
                # Fetch the PatientMaster instance using the patient_id
                patient = PatientMaster.objects.get(pk=patient_id)

                # Fetch the Doctor instance from the patient's refbydoctor field
                doctor = patient.refbydoctor  # Get the doctor from the patient's refbydoctor field

                # Create a Kidney instance without saving it yet
                kidney_test = form.save(commit=False)
                kidney_test.test_id = next_test_id
                kidney_test.patient = patient
                kidney_test.doctor = doctor  # Assign the doctor

                # Populate the Kidney instance with data from PatientMaster
                kidney_test.patientname = patient.patientname
                kidney_test.age = patient.age
                kidney_test.gender = patient.gender
                kidney_test.mobile = patient.mobile
                kidney_test.email = patient.email

                # Save the Kidney instance
                kidney_test.save()

                # Update the next_test_id for the form
                next_test_id += 1

                messages.success(request, 'Kidney test added successfully.')
                form = KidneyForm(initial={'test_id': next_test_id})
                return render(request, 'pathoapp/addkidney.html', {'form': form, 'next_test_id': next_test_id, 'patients': patients})
            except PatientMaster.DoesNotExist:
                messages.error(request, 'Patient ID not found.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    else:
        # For GET requests, initialize the form with the next_test_id
        form = KidneyForm(initial={'test_id': next_test_id})

    return render(request, 'pathoapp/addkidney.html', {'form': form, 'next_test_id': next_test_id, 'patients': patients})

def viewkidney(request):
    # Fetch all kidney tests from the database
    kidney_tests = Kidney.objects.all()

    # Pass the test data to the template for rendering
    return render(request, 'pathoapp/viewkidney.html', {
        'kidney_tests': kidney_tests
    })

def updatekidney(request, test_id):
    # Fetch the kidney test instance or show a 404 page if not found
    kidney_test = get_object_or_404(Kidney, test_id=test_id)

    if request.method == 'POST':
        # Bind form to POST data
        form = KidneyForm(request.POST, instance=kidney_test)
        if form.is_valid():
            # Save the updated test if the form is valid
            form.save()
            messages.success(request, 'Data Updated Successfully.')
            return redirect('viewkidney')
        else:
            # Add form errors to the context for debugging
            messages.error(request, 'Please correct the errors below.')
            print("Form Errors:", form.errors)  # Debugging information
    else:
        # Pre-populate the form with existing instance data
        form = KidneyForm(instance=kidney_test)

    # Fetch the patient information from the PatientMaster associated with the Kidney test
    patient_data = kidney_test.patient  # Get the associated PatientMaster instance

    # Pre-fill the form with the patient's ID (as this can be changed)
    form.fields['patient_id'].initial = patient_data.patientid  # Assign initial patient ID value
    
    # Fetch additional data (refbydoctor and doctor_email) from PatientMaster
    patient_data.refbydoctor = patient_data.refbydoctor  # Fetch referred doctor name
    patient_data.email = patient_data.email  # Fetch doctor email

    # Render the update form template with the form and patient data
    return render(request, 'pathoapp/updatekidney.html', {
        'form': form,
        'test_id': test_id,
        'patient_data': patient_data  # Pass the patient data to the template
    })

def deletekidney(request, test_id):
    # Get the kidney test record to be deleted
    kidney_test = get_object_or_404(Kidney, test_id=test_id)
    
    # Delete the record
    kidney_test.delete()
    
    # Add a success message
    messages.success(request, 'kidney test deleted successfully.')
    
    # Redirect to the view page
    return redirect('viewkidney')


def generate_kidney_report(request, test_id):
    # Fetch the Kidney test
    kidney_test = get_object_or_404(Kidney, test_id=test_id)

    # Fetch pathology info
    pathology_info = Pathoinfo.objects.first()

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="kidney_report_{test_id}.pdf"'

    # Create the report
    report = KidneyReport(response, kidney_test)
    report.generate(pathology_info)
    return response

def addurine(request):
    # Get the next test ID for the Urine test
    max_test_id = Urine.objects.aggregate(Max('test_id'))['test_id__max']
    next_test_id = (max_test_id + 1) if max_test_id is not None else 1

    # Fetch all patients from the PatientMaster model
    patients = PatientMaster.objects.all()

    if request.method == 'POST':
        form = UrineForm(request.POST)
        if form.is_valid():
            patient_id = request.POST.get('patient_id')  # Get patient_id from the form
            try:
                # Fetch the PatientMaster instance using the patient_id
                patient = PatientMaster.objects.get(pk=patient_id)

                # Fetch the Doctor instance from the patient's refbydoctor field
                doctor = patient.refbydoctor  # Get the doctor from the patient's refbydoctor field

                # Create a Urine instance without saving it yet
                urine_test = form.save(commit=False)
                urine_test.test_id = next_test_id
                urine_test.patient = patient
                urine_test.doctor = doctor  # Assign the doctor

                # Populate the Urine instance with data from PatientMaster
                urine_test.patientname = patient.patientname
                urine_test.age = patient.age
                urine_test.gender = patient.gender
                urine_test.mobile = patient.mobile
                urine_test.email = patient.email

                # Save the Urine instance
                urine_test.save()

                # Update the next_test_id for the form
                next_test_id += 1

                messages.success(request, 'Urine test added successfully.')
                form = UrineForm(initial={'test_id': next_test_id})
                return render(request, 'pathoapp/addurine.html', {'form': form, 'next_test_id': next_test_id, 'patients': patients})
            except PatientMaster.DoesNotExist:
                messages.error(request, 'Patient ID not found.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    else:
        # For GET requests, initialize the form with the next_test_id
        form = UrineForm(initial={'test_id': next_test_id})

    return render(request, 'pathoapp/addurine.html', {'form': form, 'next_test_id': next_test_id, 'patients': patients})

def viewurine(request):
    # Fetch all Urine tests from the database
    urine_test = Urine.objects.all()

    # Pass the test data to the template for rendering
    return render(request, 'pathoapp/viewurine.html', {
        'urine_tests': urine_test
    })

def updateurine(request, test_id):
    # Fetch the Urine test instance or show a 404 page if not found
    urine_test = get_object_or_404(Urine, test_id=test_id)

    if request.method == 'POST':
        # Bind form to POST data
        form = UrineForm(request.POST, instance=urine_test)
        if form.is_valid():
            # Save the updated test if the form is valid
            form.save()
            messages.success(request, 'Data Updated Successfully.')
            return redirect('viewurine')
        else:
            # Add form errors to the context for debugging
            messages.error(request, 'Please correct the errors below.')
            print("Form Errors:", form.errors)  # Debugging information
    else:
        # Pre-populate the form with existing instance data
        form = UrineForm(instance=urine_test)

    # Fetch the patient information from the PatientMaster associated with the Haematology test
    patient_data = urine_test.patient  # Get the associated PatientMaster instance

    # Pre-fill the form with the patient's ID (as this can be changed)
    form.fields['patient_id'].initial = patient_data.patientid  # Assign initial patient ID value
    
    # Fetch additional data (refbydoctor and doctor_email) from PatientMaster
    patient_data.refbydoctor = patient_data.refbydoctor  # Fetch referred doctor name
    patient_data.email = patient_data.email  # Fetch doctor email

    # Render the update form template with the form and patient data
    return render(request, 'pathoapp/updateurine.html', {
        'form': form,
        'test_id': test_id,
        'patient_data': patient_data  # Pass the patient data to the template
    })


def deleteurine(request, test_id):
    # Get the Haematology test record to be deleted
    urine_test = get_object_or_404(Urine, test_id=test_id)
    
    # Delete the record
    urine_test.delete()
    
    # Add a success message
    messages.success(request, 'Urine test deleted successfully.')
    
    # Redirect to the view page
    return redirect('viewurine')

def generate_urine_report(request, test_id):
    # Fetch the Urine test
    urine_test = get_object_or_404(Urine, test_id=test_id)

    # Fetch pathology info
    pathology_info = Pathoinfo.objects.first()

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="urine_report_{test_id}.pdf"'

    # Create the report
    report = UrineReport(response, urine_test)
    report.generate(pathology_info)
    return response

def addhiv(request):
    # Get the next test ID for the Hiv test
    max_test_id = Hiv.objects.aggregate(Max('test_id'))['test_id__max']
    next_test_id = (max_test_id + 1) if max_test_id is not None else 1

    # Fetch all patients from the PatientMaster model
    patients = PatientMaster.objects.all()

    if request.method == 'POST':
        form = HivForm(request.POST)
        if form.is_valid():
            patient_id = request.POST.get('patient_id')  # Get patient_id from the form
            try:
                # Fetch the PatientMaster instance using the patient_id
                patient = PatientMaster.objects.get(pk=patient_id)

                # Fetch the Doctor instance from the patient's refbydoctor field
                doctor = patient.refbydoctor  # Get the doctor from the patient's refbydoctor field

                # Create a Hiv instance without saving it yet
                hiv_test = form.save(commit=False)
                hiv_test.test_id = next_test_id
                hiv_test.patient = patient
                hiv_test.doctor = doctor  # Assign the doctor

                # Populate the Hiv instance with data from PatientMaster
                hiv_test.patientname = patient.patientname
                hiv_test.age = patient.age
                hiv_test.gender = patient.gender
                hiv_test.mobile = patient.mobile
                hiv_test.email = patient.email

                # Save the Hiv instance
                hiv_test.save()

                # Update the next_test_id for the form
                next_test_id += 1

                messages.success(request, 'Hiv test added successfully.')
                form = HivForm(initial={'test_id': next_test_id})
                return render(request, 'pathoapp/addhiv.html', {'form': form, 'next_test_id': next_test_id, 'patients': patients})
            except PatientMaster.DoesNotExist:
                messages.error(request, 'Patient ID not found.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    else:
        # For GET requests, initialize the form with the next_test_id
        form = HivForm(initial={'test_id': next_test_id})

    return render(request, 'pathoapp/addhiv.html', {'form': form, 'next_test_id': next_test_id, 'patients': patients})

def viewhiv(request):
    # Fetch all Hiv tests from the database
    hiv_tests = Hiv.objects.all()

    # Pass the test data to the template for rendering
    return render(request, 'pathoapp/viewhiv.html', {
        'hiv_tests': hiv_tests
    })

def updatehiv(request, test_id):
    # Fetch the Haematology test instance or show a 404 page if not found
    hiv_test = get_object_or_404(Hiv, test_id=test_id)

    if request.method == 'POST':
        # Bind form to POST data
        form = HaematologyForm(request.POST, instance=hiv_test)
        if form.is_valid():
            # Save the updated test if the form is valid
            form.save()
            messages.success(request, 'Data Updated Successfully.')
            return redirect('viewhiv')
        else:
            # Add form errors to the context for debugging
            messages.error(request, 'Please correct the errors below.')
            print("Form Errors:", form.errors)  # Debugging information
    else:
        # Pre-populate the form with existing instance data
        form = HivForm(instance=hiv_test)

    # Fetch the patient information from the PatientMaster associated with the Haematology test
    patient_data = hiv_test.patient  # Get the associated PatientMaster instance

    # Pre-fill the form with the patient's ID (as this can be changed)
    form.fields['patient_id'].initial = patient_data.patientid  # Assign initial patient ID value
    
    # Fetch additional data (refbydoctor and doctor_email) from PatientMaster
    patient_data.refbydoctor = patient_data.refbydoctor  # Fetch referred doctor name
    patient_data.email = patient_data.email  # Fetch doctor email

    # Render the update form template with the form and patient data
    return render(request, 'pathoapp/updatehiv.html', {
        'form': form,
        'test_id': test_id,
        'patient_data': patient_data  # Pass the patient data to the template
    })


def deletehiv(request, test_id):
    # Get the Hiv test record to be deleted
    hiv_test = get_object_or_404(Hiv, test_id=test_id)
    
    # Delete the record
    hiv_test.delete()
    
    # Add a success message
    messages.success(request, 'HIV test deleted successfully.')
    
    # Redirect to the view page
    return redirect('viewhiv')

def generate_hiv_report(request, test_id):
    # Fetch the HIV test
    hiv_test = get_object_or_404(Hiv, test_id=test_id)

    # Fetch pathology info
    pathology_info = Pathoinfo.objects.first()

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="hiv_report_{test_id}.pdf"'

    # Create the report
    report = HivReport(response, hiv_test)
    report.generate(pathology_info)

    return response


def addmicroalbumin(request):
   # Get the next test ID for the Microalbumin test
    max_test_id = Microalbumin.objects.aggregate(Max('test_id'))['test_id__max']
    next_test_id = (max_test_id + 1) if max_test_id is not None else 1

    # Fetch all patients from the PatientMaster model
    patients = PatientMaster.objects.all()

    if request.method == 'POST':
        form = MicroalbuminForm(request.POST)
        if form.is_valid():
            patient_id = request.POST.get('patient_id')  # Get patient_id from the form
            try:
                # Fetch the PatientMaster instance using the patient_id
                patient = PatientMaster.objects.get(pk=patient_id)

                # Fetch the Doctor instance from the patient's refbydoctor field
                doctor = patient.refbydoctor  # Get the doctor from the patient's refbydoctor field

                # Create a Microalbumin instance without saving it yet
                microalbumin_test = form.save(commit=False)
                microalbumin_test.test_id = next_test_id
                microalbumin_test.patient = patient
                microalbumin_test.doctor = doctor  # Assign the doctor

                # Populate the Microalbumin instance with data from PatientMaster
                microalbumin_test.patientname = patient.patientname
                microalbumin_test.age = patient.age
                microalbumin_test.gender = patient.gender
                microalbumin_test.mobile = patient.mobile
                microalbumin_test.email = patient.email

                # Save the Microalbumin instance
                microalbumin_test.save()

                # Update the next_test_id for the form
                next_test_id += 1

                messages.success(request, 'Microalbumin test added successfully.')
                form = MicroalbuminForm(initial={'test_id': next_test_id})
                return render(request, 'pathoapp/addmicroalbumin.html', {'form': form, 'next_test_id': next_test_id, 'patients': patients})
            except PatientMaster.DoesNotExist:
                messages.error(request, 'Patient ID not found.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    else:
        # For GET requests, initialize the form with the next_test_id
        form = MicroalbuminForm(initial={'test_id': next_test_id})

    return render(request, 'pathoapp/addmicroalbumin.html', {'form': form, 'next_test_id': next_test_id, 'patients': patients})

def viewmicroalbumin(request):
    # Fetch all Haematology tests from the database
    microalbumin_tests = Microalbumin.objects.all()

    # Pass the test data to the template for rendering
    return render(request, 'pathoapp/viewmicroalbumin.html', {
        'microalbumin_tests': microalbumin_tests
    })

def updatemicroalbumin(request, test_id):
    # Fetch the Haematology test instance or show a 404 page if not found
    microalbumin_test = get_object_or_404(Microalbumin, test_id=test_id)

    if request.method == 'POST':
        # Bind form to POST data
        form = MicroalbuminForm(request.POST, instance=microalbumin_test)
        if form.is_valid():
            # Save the updated test if the form is valid
            form.save()
            messages.success(request, 'Data Updated Successfully.')
            return redirect('viewmicroalbumin')
        else:
            # Add form errors to the context for debugging
            messages.error(request, 'Please correct the errors below.')
            print("Form Errors:", form.errors)  # Debugging information
    else:
        # Pre-populate the form with existing instance data
        form = MicroalbuminForm(instance=microalbumin_test)

    # Fetch the patient information from the PatientMaster associated with the Haematology test
    patient_data = microalbumin_test.patient  # Get the associated PatientMaster instance

    # Pre-fill the form with the patient's ID (as this can be changed)
    form.fields['patient_id'].initial = patient_data.patientid  # Assign initial patient ID value
    
    # Fetch additional data (refbydoctor and doctor_email) from PatientMaster
    patient_data.refbydoctor = patient_data.refbydoctor  # Fetch referred doctor name
    patient_data.email = patient_data.email  # Fetch doctor email

    # Render the update form template with the form and patient data
    return render(request, 'pathoapp/updatemicroalbumin.html', {
        'form': form,
        'test_id': test_id,
        'patient_data': patient_data  # Pass the patient data to the template
    })

def deletemicroalbumin(request, test_id):
    # Get the Haematology test record to be deleted
    microalbumin_test = get_object_or_404(Microalbumin, test_id=test_id)
    
    # Delete the record
    microalbumin_test.delete()
    
    # Add a success message
    messages.success(request, 'Microalbumin test deleted successfully.')
    
    # Redirect to the view page
    return redirect('viewmicroalbumin')

def generate_microalbumin_report(request, test_id):
    # Fetch the Microalbumin test
    microalbumin_test = get_object_or_404(Microalbumin, test_id=test_id)

    # Fetch pathology info
    pathology_info = Pathoinfo.objects.first()

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="microalbumin_report_{test_id}.pdf"'

    # Create the report
    report = MicroalbuminReport(response, microalbumin_test)
    report.generate(pathology_info)
    return response


def doctor_st(request):
     # Initialize variables
    doctors = Doctor.objects.all()
    selected_doctor = None
    tests = []

    if request.method == 'POST':
        # Get selected doctor's name from the form
        doctorname = request.POST.get('doctorname')
        if doctorname:
            selected_doctor = Doctor.objects.get(doctorname=doctorname)
            # Fetch tests conducted by the selected doctor
            tests = Haematology.objects.filter(doctor=selected_doctor)

    # Prepare context
    context = {
        'doctors': doctors,
        'selected_doctor': selected_doctor,
        'tests': tests,
    }

    return render(request, 'pathoapp/doctor_st.html', context)


def daily_report(request):
    # Initialize variables
    tests = []
    start_date = None
    end_date = None

    if request.method == 'POST':
        # Get start_date and end_date from the form
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Fetch tests conducted within the selected date range
        if start_date and end_date:
            tests = Haematology.objects.filter(
                test_date__gte=start_date,
                test_date__lte=end_date
            )

    # Prepare context
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'tests': tests,
    }

    return render(request, 'pathoapp/daily_report.html', context)


    
@require_GET
def get_next_test_id(request, model_name):
    """
    Generic view to get the next test_id for a given model.
    """
    try:
        # Dynamically get the model class
        model = apps.get_model('pathoapp', model_name)
        
        # Get the maximum test_id for the model
        max_test_id = model.objects.aggregate(Max('test_id'))['test_id__max']
        
        # Calculate the next test_id
        next_test_id = (max_test_id + 1) if max_test_id is not None else 1
        
        return JsonResponse({'next_test_id': next_test_id})
    except LookupError:
        return JsonResponse({'error': 'Invalid model name'}, status=400)

def addpathoinfo(request):
    if request.method == "POST":
        form = PathoinfoForm(request.POST)
        if form.is_valid():
            form.save()  # Save the data to the database
            messages.success(request, "Pathoinfo has been added successfully.")
            return redirect('pathoapp/addpathoinfo')  # Redirect to the same page or another page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PathoinfoForm()
    
    context = {
        'form': form
    }
    return render(request, 'pathoapp/addpathoinfo.html', context)  