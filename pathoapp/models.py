from django.db import models
from datetime import datetime

# Create your models here.
class Doctor(models.Model):
    doctorname = models.CharField(max_length=255, primary_key=True)  # Field for doctor's name
    email = models.EmailField(max_length=254)  # Field for doctor's email address

    def __str__(self):
        return self.doctorname

class PatientMaster(models.Model):
    patientid = models.IntegerField(primary_key=True)  
    patientname = models.CharField(max_length=100)  # Renamed 'name' to 'patientname'
    recondate = models.DateField()  # Recommended date for the patient
    age = models.IntegerField()
    
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='MALE')
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=255)

    # Reference to Doctor model
    refbydoctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.patientname} ({self.patientid})"  # Now displaying patientname

class Haematology(models.Model):
    # Linking to PatientMaster model
    patient = models.ForeignKey(PatientMaster, on_delete=models.CASCADE)
    
    # Linking to Doctor model
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)  # Add this field
   
   # Test details
    test_id = models.IntegerField(primary_key=True)  # Primary key for the test
    test_date = models.DateField(default=datetime.now)  # Automatically sets the current date

    # Haematology test fields
    haemoglobin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    rbc_count = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    platelets = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pcv = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mcv = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mch = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mchc = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    reticulocyte_count = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bleeding_time = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    clotting_time = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    eosinophil_exam = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sickling_exam = models.CharField(max_length=100, null=True, blank=True)
    other_test = models.CharField(max_length=100, null=True, blank=True)
    result = models.CharField(max_length=100, null=True, blank=True)
    normal_value = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)

    # Additional patient fields
    patientname = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"Haematology Test {self.test_id} for {self.patient.patientname}"

class Pathoinfo(models.Model):
    name = models.CharField(max_length=100)  
    add1 = models.CharField(max_length=50)
    add2 = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    phone_off = models.CharField(max_length=100)
    phone_resi = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    cgstno= models.CharField(max_length=50)
    cstno = models.CharField(max_length=50)
    panno = models.CharField(max_length=50)
    term1 = models.CharField(max_length=50)
    term2= models.CharField(max_length=50)
    
    def __str__(self):
         return self.name         

class BloodSugar(models.Model):
    # Linking to PatientMaster model
    patient = models.ForeignKey(PatientMaster, on_delete=models.CASCADE)
   
    # Test details
    test_id = models.IntegerField(primary_key=True)  # Primary key for the test
    test_date = models.DateField(default=datetime.now)  # Automatically sets the current date

    # Linking to Doctor model
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)  # Add this field
    
    # BloodSugar test fields
    bloodfas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bloodpp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bloodrandom = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    urinefas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    urinepp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    urinerandom = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    acetone = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    other_test = models.CharField(max_length=100, null=True, blank=True)
    result = models.CharField(max_length=100, null=True, blank=True)
    normal_value = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)

    # Additional patient fields
    patientname = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"BloodSugar Test {self.test_id} for {self.patient.patientname}"


class Kidney(models.Model):
    # Linking to PatientMaster model
    patient = models.ForeignKey(PatientMaster, on_delete=models.CASCADE)
   
    # Test details
    test_id = models.IntegerField(primary_key=True)  # Primary key for the test
    test_date = models.DateField(default=datetime.now)  # Automatically sets the current date

    # Linking to Doctor model
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)  # Add this field
    
    # Kidney test fields
    bloodurea = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    serumcreatinine = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bun = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    uricacid = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    other_test = models.CharField(max_length=100, null=True, blank=True)
    result = models.CharField(max_length=100, null=True, blank=True)
    normal_value = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)

    # Additional patient fields
    patientname = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"Kidney Test {self.test_id} for {self.patient.patientname}"


class Urine(models.Model):
    # Linking to PatientMaster model
    patient = models.ForeignKey(PatientMaster, on_delete=models.CASCADE)
    
    # Linking to Doctor model
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)  # Add this field
    
    # Test details
    test_id = models.IntegerField( primary_key=True)  # Primary key for the test
    test_date = models.DateField(default=datetime.now)  # Automatically sets the current date

    # Urine test fields
    colour = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    appearance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sediment = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    reaction = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    albumin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sugar = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    puscells = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    rbc = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    epithelialcells = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bilesalt = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    aceyone = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    casts = models.CharField(max_length=100, null=True, blank=True)
    crystals = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    microorganism = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bilepigment = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    occultblood = models.CharField(max_length=100, null=True, blank=True)
    other_test = models.CharField(max_length=100, null=True, blank=True)
    other_test_result = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)

    # Additional patient fields
    patientname = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f" Urine Test {self.test_id} for {self.patient.patientname}"


class Test(models.Model):
    TEST_CHOICES = [
        ('Urine', 'Urine Test'),
        ('BloodSugar', 'Blood Sugar Test'),
        ('Haematology', 'Haematology Test'),
        ('Kidney', 'Kidney Test'),
        ('BloodSugar', 'Blood Sugar Test'),
        ('Liver', 'Liver Test'),
        ('Lipid', 'Lipid Test'),
        ('Thyroid', 'Thyroid Test'),
        
        # Add other test types
    ]
    patient = models.ForeignKey(PatientMaster, on_delete=models.CASCADE, related_name='tests')
    test_type = models.CharField(max_length=50, choices=TEST_CHOICES)
    test_date = models.DateField()
        # Additional fields like test results can be added

    def __str__(self):
        return f"{self.test_type} for {self.patient.patientname} on {self.test_date}"
    
class Hiv(models.Model):
    # Linking to PatientMaster model
    patient = models.ForeignKey(PatientMaster, on_delete=models.CASCADE)
    
    # Linking to Doctor model
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)  # Add this field
    
    # Test details
    test_id = models.IntegerField(primary_key=True)  # Primary key for the test
    test_date = models.DateField(default=datetime.now)  # Automatically sets the current date

    # Hiv test fields
    hiv = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    other_test = models.CharField(max_length=100, null=True, blank=True)
    result = models.CharField(max_length=100, null=True, blank=True)
    normal_value = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)

    # Additional patient fields
    patientname = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"Hiv Test {self.test_id} for {self.patient.patientname}"
    
class Microalbumin(models.Model):
    # Linking to PatientMaster model
    patient = models.ForeignKey(PatientMaster, on_delete=models.CASCADE)
    
    # Linking to Doctor model
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)  # Add this field
    
    # Test details
    test_id = models.IntegerField(primary_key=True)  # Primary key for the test
    test_date = models.DateField(default=datetime.now)  # Automatically sets the current date

    # MicroUrine test fields
    colour = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    clarity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    albumin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    creatine = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    acratio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    other_test = models.CharField(max_length=100, null=True, blank=True)
    result = models.CharField(max_length=100, null=True, blank=True)
    normal_value = models.CharField(max_length=100, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)

    # Additional patient fields
    patientname = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"Microalbumin Test {self.test_id} for {self.patient.patientname}" 



