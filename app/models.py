from django.contrib.auth.models import AbstractBaseUser, UserManager, AbstractUser
from django.db import models


# Create your models here.


# class User(AbstractBaseUser):
#     GENDERS = (('Femenino', 'Femenino'), ('Masculino', 'Masculino'))
#     first_name = models.CharField(max_length=50, blank=True, verbose_name='Nombre')
#     last_name = models.CharField(max_length=50, blank=True, verbose_name='Apellido')
#     username = models.CharField(max_length=100, verbose_name='Nombre de Usuario', unique=True)
#     password = models.CharField(max_length=1000, verbose_name='Password')
#     gender = models.CharField(max_length=200, choices=GENDERS, null=True, verbose_name='Género')
#     date_birth = models.DateField(auto_now_add=False, null=True, verbose_name='Fecha de Nacimiento')
#     email = models.EmailField(max_length=150, verbose_name='Email')
#     dni = models.PositiveIntegerField(verbose_name='DNI', unique=True, null=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     age = models.PositiveIntegerField(verbose_name='Edad', null=True)
#     address = models.CharField(max_length=1500, verbose_name='Domicilio', null=True)
#     phone_number = models.CharField(max_length=150, verbose_name='Número de Teléfono', null=True)
#     # profile_picture = models.ImageField(upload_to="user_data/profile_picture", blank=True)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'username'
#     objects = UserManager()
#
#     def __str__(self):
#         return '{} {}'.format(self.first_name, self.last_name)
#         # return '{}'.format(self.dni)
#
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     class Meta:
#         verbose_name = 'Usuario'
#         verbose_name_plural = 'Usuarios'
#         ordering = ['id']

class User(AbstractUser):
    GENDERS = (('Femenino', 'Femenino'), ('Masculino', 'Masculino'))
    age = models.PositiveIntegerField(verbose_name='Edad', null=True)
    address = models.CharField(max_length=1500, verbose_name='Domicilio', null=True)
    phone_number = models.CharField(max_length=150, verbose_name='Número de Teléfono', null=True)
    gender = models.CharField(max_length=200, choices=GENDERS, null=True, verbose_name='Género')
    dni = models.PositiveIntegerField(verbose_name='DNI', unique=True, null=True)
    date_birth = models.DateField(auto_now_add=False, null=True, verbose_name='Fecha de Nacimiento')
    date_changed = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Modificación')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['id']


class Specialty(models.Model):
    name = models.CharField(max_length=150, verbose_name='Especialidad', unique=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'
        ordering = ['name']


class Professional(User):
    specialties = models.ManyToManyField(Specialty, verbose_name='Especialidades')
    enrollment = models.CharField(max_length=150, verbose_name='Matrícula', null=True)
    college = models.CharField(max_length=500, verbose_name='Colegio Profesional', null=True)
    other_formations = models.CharField(max_length=500, verbose_name='Otras Formaciones', null=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Profesional'
        verbose_name_plural = 'Profesionales'
        ordering = ['id']


class BodyPart(models.Model):
    name = models.CharField(max_length=150, verbose_name='Parte del Cuerpo', unique=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Parte del Cuerpo'
        verbose_name_plural = 'Partes del Cuerpo'
        ordering = ['id']


class Pathology(models.Model):
    name = models.CharField(max_length=150, verbose_name='Patología', unique=True)
    description = models.CharField(max_length=1500, verbose_name='Descripción')
    body_parts = models.ManyToManyField(BodyPart, verbose_name='Partes del Cuerpo afectadas')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Patología'
        verbose_name_plural = 'Patologías'
        ordering = ['name']


class Benefit(models.Model):
    name = models.CharField(max_length=150, verbose_name='Prestación', unique=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Prestación'
        verbose_name_plural = 'Prestaciones'
        ordering = ['name']


class Patient(User):
    WORK_ACTIVITY = (('Si', 'Si'), ('No', 'No'))
    DOMINANCE = (('Derecha', 'Derecha'), ('Izquierda', 'Izquierda'))

    contact_number = models.CharField(max_length=150, verbose_name='Número de Contacto')
    relationship = models.CharField(max_length=150, verbose_name='Parentesco')
    benefit = models.ForeignKey(Benefit, on_delete=models.CASCADE, verbose_name='Prestación')
    benefit_type = models.CharField(max_length=150, verbose_name='Detalle')
    benefit_number = models.CharField(max_length=150, verbose_name='Número de Registro')
    work_activity = models.CharField(max_length=200, choices=WORK_ACTIVITY, null=True, verbose_name='Actividad Laboral')
    work_branch = models.CharField(max_length=200, null=True, verbose_name='Rama Laboral')
    physical_activity = models.CharField(max_length=200, choices=WORK_ACTIVITY, null=True,
                                         verbose_name='¿Realiza Actividad Física?')
    competition = models.CharField(max_length=200, choices=WORK_ACTIVITY, null=True, verbose_name='¿Es Competitiva?')
    type_physical_activity = models.CharField(max_length=2000, null=True, verbose_name='Actividad Física')
    dominance = models.CharField(max_length=200, choices=DOMINANCE, null=True, verbose_name='Dominancia')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['id']


class RiskFactor(models.Model):
    risk = models.CharField(max_length=150, verbose_name='Factor de Riesgo')

    def __str__(self):
        return '{}'.format(self.risk)

    class Meta:
        verbose_name = 'Factor de Riesgo'
        verbose_name_plural = 'Factores de Riesgo'
        ordering = ['risk']


class MedicalBackground(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='Paciente')
    weight = models.FloatField(verbose_name='Peso (kg)')
    height = models.FloatField(verbose_name='Altura (m)')
    bmi = models.FloatField(verbose_name='Índice de Masa Corporal')
    abdominal_perimeter = models.FloatField(verbose_name='Perímetro Abdominal (cm)')
    measured_date = models.DateField(auto_now_add=False, null=True, verbose_name='Fecha de Medidas')
    blood_pressure_high = models.PositiveIntegerField(verbose_name='PH Alta')
    blood_pressure_low = models.PositiveIntegerField(verbose_name='PH Baja')
    medic = models.CharField(max_length=150, verbose_name='Médico de Cabecera')
    enrollment = models.CharField(max_length=150, verbose_name='Matrícula', null=True)
    risk_factors = models.ManyToManyField(RiskFactor, verbose_name='Factores de Riesgo')

    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de Carga')
    date_changed = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Modificación')


class Observation(models.Model):
    observation = models.CharField(max_length=150, verbose_name='Observaciones', blank=True)
    medical_background = models.ForeignKey(MedicalBackground, on_delete=models.CASCADE,
                                           verbose_name='Antecedentes Médicos')

    def __str__(self):
        return '{}'.format(self.observation)


class Medication(models.Model):
    medication = models.CharField(max_length=150, verbose_name='Medicaciones', blank=True)
    medical_background = models.ForeignKey(MedicalBackground, on_delete=models.CASCADE,
                                           verbose_name='Antecedentes Médicos')

    def __str__(self):
        return '{}'.format(self.medication)


class SurgicalHistory(models.Model):
    surgical_history = models.CharField(max_length=150, verbose_name='Antecedente Quirúrgico', blank=True)
    medical_background = models.ForeignKey(MedicalBackground, on_delete=models.CASCADE,
                                           verbose_name='Antecedentes Médicos')
    date_surgical = models.DateField(blank=True, null=True, verbose_name='Fecha de Cirugía')
    institution = models.CharField(blank=True, max_length=150, verbose_name='Institución')
    sequel = models.CharField(blank=True, max_length=150, verbose_name='Secuela (si hubiera)')

    def __str__(self):
        return '{}'.format(self.surgical_history)
