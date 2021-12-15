from django.conf import settings
from django.forms import *
from django.utils import timezone

from app.models import *


class ProfessionalCreateForm(ModelForm):
    password = CharField(widget=PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

        self.fields['first_name'].widget.attrs['autofocus'] = True
        self.fields['password'].widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Professional
        fields = '__all__'
        exclude = [
            'username',
            'date_joined',
            'date_changed',
        ]
        widgets = {
            'date_birth': DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'other_formations': Textarea(
                attrs={
                    'rows': 3,
                    'cols': 3,
                }),
        }


class ProfessionalUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Professional
        fields = '__all__'
        exclude = [
            'username',
            'password',
            'date_joined',
            'date_changed',
        ]
        widgets = {
            'date_birth': DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'other_formations': Textarea(
                attrs={
                    'rows': 3,
                    'cols': 3,
                }),
        }


class PatientCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Patient
        fields = '__all__'
        exclude = [
            'username',
            'password',
            'date_joined',
            'date_changed',
        ]
        widgets = {
            'date_birth': DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),

        }

    # def save(self, commit=True):
    #     data = {}
    #     form = super()
    #     try:
    #         if form.is_valid():
    #             user = form.save(commit=False)
    #             user.username = user.dni
    #             user.date_joined = timezone.now()
    #             user.date_changed = timezone.now()
    #             user.set_password('12345')
    #             user.is_active = True
    #             user.save()
    #             data['patient_id'] = str(user.id)
    #         else:
    #             data['error'] = form.errors
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return data


class PatientUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'date_birth': DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                user = form.save(commit=False)
                #user.username = user.dni
                user.date_changed = timezone.now()
                #user.set_password(user.password)
                #user.is_active = True
                user.save()
                data['patient_id'] = str(user.id)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SpecialtyCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Specialty
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class PathologyCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Pathology
        fields = '__all__'
        widgets = {
            'description': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                    'rows': 3,
                    'cols': 3,

                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class MedicalBackgroundCreateForm(ModelForm):
    qs_risk = RiskFactor.objects.all()
    risk_factors = ModelMultipleChoiceField(widget=CheckboxSelectMultiple(), queryset=qs_risk,
                                            label='Factores de Riesgo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            if form.name != 'risk_factors':
                form.field.widget.attrs['class'] = 'form-control'
                form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['risk_factors'].required = False

    class Meta:
        model = MedicalBackground
        fields = '__all__'
        exclude = [
            'patient',
        ]
        widgets = {
            'measured_date': DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        }


class BaseObservationFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Observation.objects.none()


class BaseMedicationFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Medication.objects.none()


class BaseSurgicalHistoryFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = SurgicalHistory.objects.none()


ObservationFormSet = modelformset_factory(
    Observation,
    fields='__all__',
    extra=1,
    exclude=[
        'medical_background',
    ],
    widgets={'observation': TextInput(attrs={'class': 'form-control'})},
    formset=BaseObservationFormSet

)
ObservationUpdateFormSet = modelformset_factory(
    Observation,
    fields='__all__',
    extra=0,
    exclude=[
        'medical_background',
    ],
    widgets={'observation': TextInput(attrs={'class': 'form-control'})},
    can_delete=True
    # formset=BaseObservationFormSet

)

MedicationFormSet = modelformset_factory(
    Medication,
    fields='__all__',
    extra=1,
    exclude=[
        'medical_background',
    ],
    widgets={'medication': TextInput(attrs={'class': 'form-control'})},
    formset=BaseMedicationFormSet

)
MedicationUpdateFormSet = modelformset_factory(
    Medication,
    fields='__all__',
    extra=0,
    exclude=[
        'medical_background',
    ],
    widgets={'medication': TextInput(attrs={'class': 'form-control'})},
    can_delete=True

)

SurgicalHistoryFormSet = modelformset_factory(
    SurgicalHistory,
    fields='__all__',
    extra=1,
    exclude=[
        'medical_background',
    ],
    widgets={
        'surgical_history': TextInput(attrs={'class': 'form-control'}),
        'institution': TextInput(attrs={'class': 'form-control'}),
        'sequel': TextInput(attrs={'class': 'form-control'}),
        'date_surgical': DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'})
    },
    formset=BaseSurgicalHistoryFormSet

)
SurgicalHistoryUpdateFormSet = modelformset_factory(
    SurgicalHistory,
    fields='__all__',
    extra=0,
    exclude=[
        'medical_background',
    ],
    widgets={
        'surgical_history': TextInput(attrs={'class': 'form-control'}),
        'institution': TextInput(attrs={'class': 'form-control'}),
        'sequel': TextInput(attrs={'class': 'form-control'}),
        'date_surgical': DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'})
    },
    can_delete=True

)
