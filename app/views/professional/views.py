from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from app.forms import *
from app.mixins import *


# Create your views here.


class IndexView(TemplateView):
    template_name = 'site/index.html'


class ProfessionalListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Professional
    template_name = 'professional/list.html'
    permission_required = 'app.view_professional'

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Profesionales'
        context['create_url'] = reverse_lazy('app:professional_create')
        context['list_url'] = reverse_lazy('app:professional_list')
        context['entity'] = 'Listado'
        context['prev_entity'] = 'Profesionales'
        return context


class ProfessionalCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Professional
    form_class = ProfessionalCreateForm
    template_name = 'professional/create.html'
    success_url = reverse_lazy('app:professional_list')
    url_redirect = success_url
    permission_required = 'app.add_professional'

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = {}
        try:
            context = self.get_context_data()
            if form.is_valid():
                professional = form.save(commit=False)
                professional.username = professional.dni
                professional.date_joined = timezone.now()
                professional.date_changed = timezone.now()
                professional.set_password(professional.password)
                professional.is_active = True
                professional.save()
                form.save_m2m()
                messages.add_message(self.request, messages.INFO, 'Profesional Creado correctamente.',
                                     extra_tags='success')
        except Exception as e:
            data['error'] = str(e)
            messages.add_message(self.request, messages.INFO, str(e),
                                 extra_tags='error')
            return redirect('app:professional_list')

        return redirect('app:professional_list')

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        context = super(ProfessionalCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Nuevo Profesional'
        context['entity'] = 'Profesionales'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ProfessionalUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Professional
    form_class = ProfessionalUpdateForm
    template_name = 'professional/update.html'
    success_url = reverse_lazy('app:professional_list')

    url_redirect = success_url
    permission_required = 'app.change_professional'

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = {}
        try:
            context = self.get_context_data()
            if form.is_valid():
                professional = form.save(commit=False)
                professional.date_changed = timezone.now()
                professional.username = professional.dni
                professional.save()
                form.save_m2m()
                messages.add_message(self.request, messages.INFO, 'Profesional Editado correctamente.',
                                     extra_tags='success')
        except Exception as e:
            data['error'] = str(e)
            messages.add_message(self.request, messages.INFO, str(e),
                                 extra_tags='error')
            return redirect('app:professional_list')

        return redirect('app:professional_list')

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        context = super(ProfessionalUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Editar Profesional'
        context['entity'] = 'Profesionales'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['c_date'], context['m_date'] = self.getDates
        return context

    @property
    def getDates(self):
        c_date = self.object.date_joined
        m_date = self.object.date_changed
        return c_date, m_date


class ProfessionalDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Professional
    template_name = 'professional/delete.html'
    success_url = reverse_lazy('app:professional_list')
    permission_required = 'app.delete_professional'

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            messages.add_message(self.request, messages.INFO, 'Profesional Eliminado correctamente.',
                                 extra_tags='success')
        except Exception as e:
            data['error'] = str(e)
            messages.add_message(self.request, messages.INFO, str(e),
                                 extra_tags='error')
        # return JsonResponse(data)
        return redirect('app:professional_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Profesional'
        context['entity'] = 'Eliminar Profesional'
        context['prev_entity'] = 'Profesional'
        context['message'] = 'Profesional'
        context['list_url'] = reverse_lazy('app:professional_list')
        return context
