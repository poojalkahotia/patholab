from django import forms
from .models import *
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class ForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
    )

class ResetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
    )
    
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['doctorname', 'email']
        widgets = {
            'doctorname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }   

class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientMaster
        fields = ['patientid', 'patientname', 'recondate', 'age', 'gender', 'mobile', 'email', 'address', 'refbydoctor']
        widgets = {
            'patientid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Patient ID'}),
            'patientname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Patient Name'}),  # Updated field name
            'recondate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Age'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter Address'}),
            'refbydoctor': forms.Select(attrs={'class': 'form-control'}),
        }

class HaematologyForm(forms.ModelForm):
    class Meta:
        model = Haematology
        fields = [
            'test_date', 'haemoglobin', 'rbc_count', 'platelets',
            'pcv', 'mcv', 'mch', 'mchc', 'reticulocyte_count', 'bleeding_time', 'clotting_time',
            'eosinophil_exam', 'sickling_exam', 'other_test', 'result', 'normal_value', 'remarks'
        ]
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'haemoglobin': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'rbc_count': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'platelets': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pcv': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'mcv': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'mch': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'mchc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reticulocyte_count': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'bleeding_time': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'clotting_time': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'eosinophil_exam': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sickling_exam': forms.TextInput(attrs={'class': 'form-control'}),
            'other_test': forms.TextInput(attrs={'class': 'form-control'}),
            'result': forms.TextInput(attrs={'class': 'form-control'}),
            'normal_value': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'test_date': 'Test Date',
            'haemoglobin': 'Haemoglobin (g/dL)',
            'rbc_count': 'RBC Count (million/µL)',
            'platelets': 'Platelets (per µL)',
            'pcv': 'PCV (%)',
            'mcv': 'MCV (fL)',
            'mch': 'MCH (pg)',
            'mchc': 'MCHC (g/dL)',
            'reticulocyte_count': 'Reticulocyte Count (%)',
            'bleeding_time': 'Bleeding Time (minutes)',
            'clotting_time': 'Clotting Time (minutes)',
            'eosinophil_exam': 'Eosinophil Exam (%)',
            'sickling_exam': 'Sickling Exam',
            'other_test': 'Other Test',
            'result': 'Result',
            'normal_value': 'Normal Value',
            'remarks': 'Remarks',
        }
        help_texts = {
            'haemoglobin': 'Normal range: 12-16 g/dL for females, 13-17 g/dL for males.',
            'rbc_count': 'Normal range: 4.1-5.1 million/µL for females, 4.5-5.9 million/µL for males.',
            'platelets': 'Normal range: 150,000-450,000 per µL.',
            'pcv': 'Normal range: 36-46% for females, 40-50% for males.',
            'mcv': 'Normal range: 80-100 fL.',
            'mch': 'Normal range: 27-33 pg.',
            'mchc': 'Normal range: 32-36 g/dL.',
            'reticulocyte_count': 'Normal range: 0.5-1.5%.',
            'bleeding_time': 'Normal range: 2-7 minutes.',
            'clotting_time': 'Normal range: 8-15 minutes.',
            'eosinophil_exam': 'Normal range: 1-6%.',
        }
        

class PathoinfoForm(forms.ModelForm):
    class Meta:
        model = Pathoinfo
        fields = [ 'name', 'add1', 'add2', 'city', 'phone_off', 'phone_resi', 'mobile', 'cgstno', 'cstno', 'panno',  'term1', 'term2']
        widgets = {
            
            'name': forms.TextInput(attrs={'class': 'form-control'}),  # Updated field name
            'add1': forms.Textarea(attrs={'class': 'form-control'}),   
            'add2': forms.Textarea(attrs={'class': 'form-control'}),   
            'city': forms.TextInput(attrs={'class': 'form-control'}),  # Updated field name
            'phone_off': forms.TextInput(attrs={'class': 'form-control'}),  # Updated field name
            'phone_resi': forms.TextInput(attrs={'class': 'form-control'}),  # Updated field name
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'cgstno': forms.TextInput(attrs={'class': 'form-control'}),  # Updated field name
            'cstno': forms.TextInput(attrs={'class': 'form-control'}),  # Updated field name
            'panno': forms.TextInput(attrs={'class': 'form-control'}),  # Updated field name
            'term1': forms.TextInput(attrs={'class': 'form-control'}),  # Updated field name
            'term2': forms.TextInput(attrs={'class': 'form-control'}),  # Updated field name
            
         }


class BloodSugarForm(forms.ModelForm):
    class Meta:
        model = BloodSugar
        fields = [
            'test_id', 'test_date', 'doctor', 'bloodfas', 'bloodpp', 'bloodrandom',
            'urinefas', 'urinepp', 'urinerandom', 'acetone', 'other_test', 'result',
            'normal_value', 'remarks', 'patientname', 'age', 'gender', 'mobile', 'email'
        ]
        widgets = {
            'test_id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'doctor': forms.TextInput(attrs={'readonly': 'readonly'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

class KidneyForm(forms.ModelForm):
    class Meta:
        model = Kidney
        fields = [
            'test_id', 'test_date', 'doctor', 'bloodurea', 'serumcreatinine', 'bun',
            'uricacid', 'other_test', 'result', 'normal_value', 'remarks',
            'patientname', 'age', 'gender', 'mobile', 'email'
        ]
        widgets = {
            'test_id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'doctor': forms.TextInput(attrs={'readonly': 'readonly'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }
        
class UrineForm(forms.ModelForm):
    class Meta:
        model = Urine
        fields = [
            'test_id', 'test_date', 'doctor', 'colour', 'appearance', 'sediment',
            'reaction', 'albumin', 'sugar', 'puscells', 'rbc', 'epithelialcells',
            'bilesalt', 'aceyone', 'casts', 'crystals', 'microorganism', 'bilepigment',
            'occultblood', 'other_test', 'other_test_result', 'remarks',
            'patientname', 'age', 'gender', 'mobile', 'email'
        ]
        widgets = {
            'test_id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'doctor': forms.TextInput(attrs={'readonly': 'readonly'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

class HivForm(forms.ModelForm):
    class Meta:
        model = Hiv
        fields = [
            'test_id', 'test_date', 'doctor', 'hiv', 'other_test', 'result',
            'normal_value', 'remarks', 'patientname', 'age', 'gender', 'mobile', 'email'
        ]
        widgets = {
            'test_id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'doctor': forms.TextInput(attrs={'readonly': 'readonly'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

class MicroalbuminForm(forms.ModelForm):
    class Meta:
        model = Microalbumin
        fields = [
            'test_id', 'test_date', 'doctor', 'colour', 'clarity', 'albumin',
            'creatine', 'acratio', 'other_test', 'result', 'normal_value', 'remark',
            'patientname', 'age', 'gender', 'mobile', 'email'
        ]
        widgets = {
            'test_id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'doctor': forms.TextInput(attrs={'readonly': 'readonly'}),
            'remark': forms.Textarea(attrs={'rows': 3}),
        }