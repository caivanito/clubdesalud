import django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.forms import *
from app.mixins import *


class MedicalBackgroundListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = MedicalBackground
    permission_required = 'app.view_medicalbackground'
    template_name = 'medicalbackground/list.html'

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = Patient.objects.get(id=self.getPatientId)

        context['title'] = 'Antecedentes Médicos del Paciente: ' + str(patient)
        context['create_url'] = redirect('app:addMedicalBackground', pk=patient.id).url
        # context['list_url'] = reverse_lazy('app:patient_list')
        context['list_url'] = redirect('app:patient_list').url
        context['next'] = redirect('app:patient_list').url
        context['prev_entity'] = 'Pacientes'
        context['entity'] = 'Antecedentes Médicos'

        context['object_list'] = MedicalBackground.objects.filter(patient_id=patient.id)
        context['patient'] = patient

        return context

    @property
    def getPatientId(self):
        return self.kwargs.get('pk')  # El que estás pasando en tu URL


class MedicalBackgroundCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = MedicalBackground
    form_class = MedicalBackgroundCreateForm
    template_name = 'medicalbackground/addMedicalBackground.html'
    success_url = reverse_lazy('app:patient_list')
    permission_required = 'app.add_medicalbackground'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = {}
        try:
            context = self.get_context_data()
            observation_formset = context['observation_formset']
            medication_formset = context['medication_formset']
            surgical_formset = context['surgical_formset']

            if form.is_valid and observation_formset.is_valid() and medication_formset.is_valid() and surgical_formset.is_valid():
                medical_background = form.save(commit=False)
                medical_background.patient = Patient.objects.get(id=self.getPatientId)
                medical_background.date_changed = django.utils.timezone.now()
                medical_background = form.save()

                flag_duplicate = False
                flag_unique = False
                index = 1
                for form in observation_formset.forms:
                    total_forms = len(observation_formset.forms)

                    if total_forms == 1:
                        obs = form.save(commit=False)
                        obs.medical_background = medical_background
                        if obs.observation == '':
                            obs.observation = 'Ninguna'
                        obs.save()
                    else:
                        if index == total_forms and flag_unique is False:
                            flag_duplicate = True
                        obs = form.save(commit=False)
                        obs.medical_background = medical_background
                        if obs.observation == '':
                            if flag_duplicate and index == total_forms:
                                obs.observation = 'Ninguna'
                                flag_duplicate = False
                                obs.save()
                        else:
                            flag_unique = True
                            obs.save()
                    index += 1

                flag_duplicate = False
                flag_unique = False
                index = 1
                for form in medication_formset.forms:
                    total_forms = len(medication_formset.forms)

                    if total_forms == 1:
                        medication = form.save(commit=False)
                        medication.medical_background = medical_background
                        if medication.medication == '':
                            medication.medication = 'Ninguna'
                        medication.save()
                    else:
                        if index == total_forms and flag_unique is False:
                            flag_duplicate = True

                        medication = form.save(commit=False)
                        medication.medical_background = medical_background
                        if medication.medication == '':
                            if flag_duplicate and index == total_forms:
                                medication.medication = 'Ninguna'
                                flag_duplicate = False
                                medication.save()
                        else:
                            flag_unique = True
                            medication.save()
                    index += 1

                flag_duplicate = False
                flag_unique = False
                index = 1
                for form in surgical_formset.forms:
                    total_forms = len(surgical_formset.forms)

                    if total_forms == 1:
                        surgical = form.save(commit=False)
                        surgical.medical_background = medical_background
                        if surgical.surgical_history == '':
                            surgical.surgical_history = 'Ninguna'
                        surgical.save()
                    else:
                        if index == total_forms and flag_unique is False:
                            flag_duplicate = True
                        surgical = form.save(commit=False)
                        surgical.medical_background = medical_background
                        if surgical.surgical_history == '':
                            if flag_duplicate and index == total_forms:
                                surgical.surgical_history = 'Ninguna'
                                flag_duplicate = False
                                surgical.save()
                        else:
                            flag_unique = True
                            surgical.save()
                    index += 1
                messages.add_message(self.request, messages.INFO,
                                     'Paciente Creado correctamente',
                                     extra_tags='success')
        except Exception as e:
            data['error'] = str(e)
            messages.add_message(self.request, messages.INFO, str(e),
                                 extra_tags='error')
            return redirect('app:patient_list')

        return super(MedicalBackgroundCreateView, self).form_valid(form)
        # return redirect('app:addSurgicalHistory', pk=self.getPatientId)  # funciona

    def get_context_data(self, **kwargs):
        context = super(MedicalBackgroundCreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['observation_formset'] = ObservationFormSet(self.request.POST, prefix='observation')
            context['medication_formset'] = MedicationFormSet(self.request.POST, prefix='medication')
            context['surgical_formset'] = SurgicalHistoryFormSet(self.request.POST, prefix='surgical')
        else:
            context['observation_formset'] = ObservationFormSet(prefix='observation')
            context['medication_formset'] = MedicationFormSet(prefix='medication')
            context['surgical_formset'] = SurgicalHistoryFormSet(prefix='surgical')

        patient = Patient.objects.get(id=self.getPatientId)
        context['title'] = 'Antecedentes Médicos del Paciente: ' + str(patient)
        context['entity'] = 'Antecedentes Médicos'
        context['prev_entity'] = 'Nuevo Paciente'
        context['list_url'] = self.success_url
        context['next'] = self.success_url
        context['action'] = 'add'
        return context

    @property
    def getPatientId(self):
        return self.kwargs.get('pk')  # El que estás pasando en tu URL


class MedicalBackgroundUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = MedicalBackground
    form_class = MedicalBackgroundCreateForm
    template_name = 'medicalbackground/updateMedicalBackground.html'
    success_url = reverse_lazy('app:patient_list')
    permission_required = 'app.change_medicalbackground'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = {}
        try:
            context = self.get_context_data()
            observation_formset = context['observation_formset']
            medication_formset = context['medication_formset']
            surgical_formset = context['surgical_formset']
            print(str(observation_formset.is_valid()))
            print(str(observation_formset.errors))
            print(str(medication_formset.is_valid()))
            print(str(surgical_formset.is_valid()))
            print(str(surgical_formset.errors))

            if form.is_valid and observation_formset.is_valid() and medication_formset.is_valid() and surgical_formset.is_valid():
                medical_background = form.save(commit=False)
                medical_background.date_changed = django.utils.timezone.now()
                medical_background = form.save()

                flag_duplicate = False
                flag_unique = False
                index = 1
                for form in observation_formset.forms:
                    if form in observation_formset.deleted_forms:
                        _form = form.instance
                        _form.delete()
                    else:
                        total_forms = len(observation_formset.forms)
                        if total_forms == 1:
                            obs = form.save(commit=False)
                            if obs.observation == '':
                                obs.observation = 'Ninguna'
                            obs.save()
                        else:
                            if index == total_forms and flag_unique is False:
                                flag_duplicate = True
                            obs = form.save(commit=False)
                            obs.medical_background = medical_background
                            if obs.observation == '':
                                if flag_duplicate and index == total_forms:
                                    obs.observation = 'Ninguna'
                                    flag_duplicate = False
                                    obs.save()
                            else:
                                flag_unique = True
                                obs.save()
                    index += 1

                flag_duplicate = False
                flag_unique = False
                index = 1
                for form in medication_formset.forms:
                    if form in medication_formset.deleted_forms:
                        _form = form.instance
                        _form.delete()
                    else:
                        total_forms = len(medication_formset.forms)
                        if total_forms == 1:
                            medication = form.save(commit=False)
                            medication.medical_background = medical_background
                            if medication.medication == '':
                                medication.medication = 'Ninguna'
                            medication.save()
                        else:
                            if index == total_forms and flag_unique is False:
                                flag_duplicate = True
                            medication = form.save(commit=False)
                            medication.medical_background = medical_background
                            if medication.medication == '':
                                if flag_duplicate and index == total_forms:
                                    medication.medication = 'Ninguna'
                                    flag_duplicate = False
                                    medication.save()
                            else:
                                flag_unique = True
                                medication.save()
                    index += 1

                flag_duplicate = False
                flag_unique = False
                index = 1
                for form in surgical_formset.forms:
                    if form in surgical_formset.deleted_forms:
                        _form = form.instance
                        _form.delete()
                    else:
                        total_forms = len(surgical_formset.forms)
                        if total_forms == 1:
                            surgical = form.save(commit=False)
                            if surgical.surgical_history == '':
                                surgical.surgical_history = 'Ninguna'
                            surgical.save()
                        else:
                            if index == total_forms and flag_unique is False:
                                flag_duplicate = True
                            surgical = form.save(commit=False)
                            if surgical.surgical_history == '':
                                if flag_duplicate and index == total_forms:
                                    surgical.surgical_history = 'Ninguna'
                                    flag_duplicate = False
                                    surgical.save()
                            else:
                                flag_unique = True
                                surgical.save()
                    index += 1
                messages.add_message(self.request, messages.INFO,
                                     'Historia Clínica Editada correctamente',
                                     extra_tags='success')
        except Exception as e:
            data['error'] = str(e)
            messages.add_message(self.request, messages.INFO, str(e),
                                 extra_tags='error')
            return redirect('app:listMedicalBackground', pk=self.getPK)


        # return super(MedicalBackgroundUpdateView, self).form_valid(form)
        # return redirect('app:addSurgicalHistory', pk=self.getPatientId)  # funciona
        #return redirect('app:patient_list')
        return redirect('app:listMedicalBackground', pk=self.getPK)

    def get_context_data(self, **kwargs):
        # context = super(MedicalBackgroundUpdateView, self).get_context_data(**kwargs)
        # context = super().get_context_data(**kwargs)
        context = super(MedicalBackgroundUpdateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['observation_formset'] = ObservationUpdateFormSet(self.request.POST,
                                                                      prefix='observation')
            context['medication_formset'] = MedicationUpdateFormSet(self.request.POST,
                                                                    prefix='medication')
            context['surgical_formset'] = SurgicalHistoryUpdateFormSet(self.request.POST,
                                                                       prefix='surgical')
        else:
            qs_obs = Observation.objects.filter(medical_background_id=self.getPK)
            qs_med = Medication.objects.filter(medical_background_id=self.getPK)
            qs_surg = SurgicalHistory.objects.filter(medical_background_id=self.getPK)

            context['observation_formset'] = ObservationUpdateFormSet(prefix='observation', queryset=qs_obs)
            context['medication_formset'] = MedicationUpdateFormSet(prefix='medication', queryset=qs_med)
            context['surgical_formset'] = SurgicalHistoryUpdateFormSet(prefix='surgical', queryset=qs_surg)

        patient = MedicalBackground.objects.get(id=self.getPK).patient.__str__()
        context['title'] = 'Editar Antecedentes Médicos del Paciente: ' + str(patient)
        context['entity'] = 'Antecedentes Médicos'
        context['prev_entity'] = 'Paciente'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['next'] = self.success_url
        context['c_date'], context['m_date'] = self.getDates

        return context

    @property
    def getPK(self):
        return self.kwargs.get('pk')  # El que estás pasando en tu URL

    @property
    def getDates(self):
        c_date = self.object.date_created
        m_date = self.object.date_changed
        return c_date, m_date


class MedicalBackgroundDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = MedicalBackground
    template_name = 'medicalbackground/delete.html'
    permission_required = 'app.delete_medicalbackground'
    success_url = reverse_lazy('app:patient_list')

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            messages.add_message(self.request, messages.INFO, 'Historia Clínica Eliminada correctamente.',
                                 extra_tags='success')
        except Exception as e:
            data['error'] = str(e)
            messages.add_message(self.request, messages.INFO, str(e),
                                 extra_tags='error')
        # return JsonResponse(data)
        return redirect('app:patient_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Paciente'
        context['entity'] = 'Eliminar Paciente'
        context['prev_entity'] = 'Paciente'
        context['message'] = 'Paciente'
        context['list_url'] = reverse_lazy('app:patient_list')
        return context
