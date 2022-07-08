from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from main.filters import RoleRequestFilter, CarFilter, EmployeeFilter
from main.forms import UserForm, CarForm
from main.models import User, Car, Administrator, RoleRequest, Client, Employee

# Create your views here.
from main.tables import RoleRequestTable, CarTable, EmployeeTable


class Index(TemplateView):
    template_name = 'index.html'


class SignIn(CreateView):
    model = User
    form_class = UserForm


class ViewAccountDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User

    def test_func(self):
        return self.request.user.id is int(self.kwargs['pk'])


class ViewCarsList(LoginRequiredMixin, UserPassesTestMixin, SingleTableMixin, FilterView):
    model = Car
    table_class = CarTable
    filterset_class = CarFilter

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(client=Client.objects.get(user=self.kwargs['pk']), deleted=False) \
            .order_by('-deleted')

    def test_func(self):
        return self.request.user.id is int(self.kwargs['pk']) and \
               not (Client.objects.filter(user=self.request.user) is None)


class ViewEmployeeList(LoginRequiredMixin, UserPassesTestMixin, SingleTableMixin, FilterView):
    model = Employee
    table_class = EmployeeTable
    filterset_class = EmployeeFilter

    def test_func(self):
        return not (Administrator.objects.filter(user=self.request.user) is None)


class AddCar(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = 'main/car_add.html'

    def test_func(self):
        return self.request.user.id is int(self.kwargs['pk']) and \
               not (Client.objects.filter(user=self.request.user) is None)

    def form_valid(self, form):
        form.instance.client = Client.objects.get(user=self.request.user)
        return super().form_valid(form)


class UpdateCar(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'main/car_update.html'

    def test_func(self):
        return self.request.user.id is int(self.kwargs['user']) and \
               not (Client.objects.filter(user=self.request.user) is None)

    def form_valid(self, form):
        form.instance.updated = timezone.now()
        return super().form_valid(form)


class DeleteCar(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/car_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car'] = Car.objects.get(id=kwargs['pk'])
        return context

    def test_func(self):
        return self.request.user.id is int(self.kwargs['user']) and \
               not (Client.objects.filter(user=self.request.user) is None)

    @staticmethod
    def post(request, *args, **kwargs):
        Car.objects.filter(id=kwargs['pk']).update(deleted=True)
        return HttpResponseRedirect(reverse('cars', kwargs={'pk': kwargs['user']}))


class ViewRoleRequestList(LoginRequiredMixin, UserPassesTestMixin, SingleTableMixin, FilterView):
    model = RoleRequest
    table_class = RoleRequestTable
    filterset_class = RoleRequestFilter

    def post(self, request, *args, **kwargs):
        if request.POST['request'] and request.POST['response']:
            id = int(request.POST['request'])
            response = request.POST['response']
            request = RoleRequest.objects.filter(id=id)
            if response == "accept":
                request.update(is_accepted=True, is_reviewed=True, updated=timezone.now())
                Client.objects.get(user=request.first().user).delete()
                if request.first().role == RoleRequest.ADMINISTRATOR:
                    Administrator.objects.create(user=request.first().user)
                else:
                    Employee.objects.create(user=request.first().user)
            else:
                request.update(is_reviewed=True, updated=timezone.now())

        return HttpResponseRedirect(reverse('roles', kwargs={'pk': self.request.user.id}))

    def test_func(self):
        return not (Administrator.objects.filter(user=self.request.user) is None)
