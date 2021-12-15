from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView

from app.mixins import *
from app.models import *
from app.forms import *


# Create your views here.

class PatientListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Patient
    template_name = 'patient/list.html'
    permission_required = 'app.view_patient'

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Pacientes'
        context['create_url'] = reverse_lazy('app:patient_create')
        context['list_url'] = reverse_lazy('app:patient_list')
        context['prev_entity'] = 'Pacientes'
        context['entity'] = 'Listado'
        return context


class PatientCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Patient
    form_class = PatientCreateForm
    template_name = 'patient/create.html'
    permission_required = 'app.add_patient'
    success_url = reverse_lazy('app:patient_list')

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = {}
        try:
            context = self.get_context_data()
            if form.is_valid():
                patient = form.save(commit=False)
                patient.username = patient.dni
                patient.date_joined = timezone.now()
                patient.date_changed = timezone.now()
                patient.set_password('12345')
                patient.is_active = True
                patient.save()
                data['patient_id'] = str(patient.id)
                messages.add_message(self.request, messages.INFO,
                                     'Paciente Creado correctamente. Por favor, complete la Historia Clínica.',
                                     extra_tags='success')
        except Exception as e:
            data['error'] = str(e)
            messages.add_message(self.request, messages.INFO, str(e),
                                 extra_tags='error')
            return redirect('app:patient_list')

        return redirect('app:addMedicalBackground', pk=data['patient_id'])  # funciona

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Paciente - Datos Personales'
        context['prev_entity'] = 'Pacientes'
        context['entity'] = 'Nuevo Paciente'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class PatientDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Patient
    template_name = 'patient/delete.html'
    permission_required = 'app.delete_patient'
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
            messages.add_message(self.request, messages.INFO, 'Paciente Eliminado correctamente.',
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


class PatientUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientUpdateForm
    template_name = 'patient/create.html'
    permission_required = 'app.change_patient'
    success_url = reverse_lazy('app:patient_list')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = {}
        try:
            context = self.get_context_data()
            if form.is_valid():
                patient = form.save(commit=False)
                patient.username = patient.dni
                patient.date_joined = timezone.now()
                patient.date_changed = timezone.now()
                patient.set_password('12345')
                patient.is_active = True
                patient.save()
                data['patient_id'] = str(patient.id)
                messages.add_message(self.request, messages.INFO, 'Paciente Editado correctamente.',
                                     extra_tags='success')
        except Exception as e:
            data['error'] = str(e)
            messages.add_message(self.request, messages.INFO, str(e),
                                 extra_tags='error')
            return redirect('app:patient_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Paciente'
        context['entity'] = 'Editar Paciente'
        context['prev_entity'] = 'Pacientes'
        context['list_url'] = reverse_lazy('app:patient_list')
        context['action'] = 'edit'
        return context
