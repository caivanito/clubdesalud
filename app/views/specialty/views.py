from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from app.models import *
from app.forms import *


# Create your views here.


class SpecialtyListView(ListView):
    model = Specialty
    template_name = 'specialty/list.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Especialidades'
        context['create_url'] = reverse_lazy('app:specialty_create')
        context['list_url'] = reverse_lazy('app:specialty_list')
        context['entity'] = 'Especialidades'
        return context


class SpecialtyCreateView(CreateView):
    model = Specialty
    form_class = SpecialtyCreateForm
    template_name = 'specialty/create.html'
    success_url = reverse_lazy('app:specialty_list')
    # permission_required = 'add_professional'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Especialidad'
        context['entity'] = 'Especialidades'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
