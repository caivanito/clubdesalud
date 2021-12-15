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


class PathologyListView(ListView):
    model = Pathology
    template_name = 'Pathology/list.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Patologías'
        context['create_url'] = reverse_lazy('app:pathology_create')
        context['list_url'] = reverse_lazy('app:pathology_list')
        context['entity'] = 'Patologías'
        return context


class PathologyCreateView(CreateView):
    model = Pathology
    form_class = PathologyCreateForm
    template_name = 'pathology/create.html'
    success_url = reverse_lazy('app:pathology_list')
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
        context['title'] = 'Nueva Patología'
        context['entity'] = 'Patologías'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
