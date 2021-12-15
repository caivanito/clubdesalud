from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from app.models import *


# Create your views here.


class IndexView(TemplateView):
    template_name = 'site/index.html'


class ProfessionalListView(ListView):
    model = Professional
    template_name = 'professional/list.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Profesionales'
        # context['create_url'] = reverse_lazy('erp:category_create')
        context['list_url'] = reverse_lazy('app:professional_list')
        context['entity'] = 'Profesionales'
        return context
