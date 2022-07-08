from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from main.filters import RoleRequestFilter, CarFilter, EmployeeFilter, AdministratorFilter
from main.forms import UserForm, CarForm
from main.models import User, Car, Administrator, RoleRequest, Client, Employee

# Create your views here.
from main.tables import RoleRequestTable, CarTable, EmployeeTable, AdministratorTable


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
               Client.objects.filter(user=self.request.user).exists()


class ViewEmployeeList(LoginRequiredMixin, UserPassesTestMixin, SingleTableMixin, FilterView):
    model = Employee
    table_class = EmployeeTable
    filterset_class = EmployeeFilter

    def test_func(self):
        return Administrator.objects.filter(user=self.request.user).exists()


class ViewAdministratorsList(LoginRequiredMixin, UserPassesTestMixin, SingleTableMixin, FilterView):
    model = Administrator
    table_class = AdministratorTable
    filterset_class = AdministratorFilter

    def test_func(self):
        return Administrator.objects.filter(user=self.request.user).exists()

    def get_queryset(self):
        qs = super().get_queryset()
        admin = Administrator.objects.get(user=self.request.user)
        return qs.exclude(id=admin.id)


class DeleteEmployee(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'main/employee_confirm_delete.html'
    model = Employee

    def test_func(self):
        return Administrator.objects.filter(user=self.request.user).exists()

    def get_success_url(self):
        Client.objects.create(user=Employee.objects.get(id=self.kwargs['pk']).user)
        return reverse_lazy('employees')


class DeleteAdministrator(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'main/administrator_confirm_delete.html'
    model = Administrator

    def test_func(self):
        return Administrator.objects.filter(user=self.request.user).exists()

    def get_success_url(self):
        Client.objects.create(user=Administrator.objects.get(id=self.kwargs['pk']).user)
        return reverse_lazy('administrators')


class DeleteCar(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'main/car_confirm_delete.html'
    model = Car

    def test_func(self):
        return self.request.user.id is int(self.kwargs['user']) and \
               Client.objects.filter(user=self.request.user).exists()

    def get_success_url(self):
        return reverse_lazy('cars', kwargs={'pk': self.request.user.id})


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


class ViewRoleRequestList(LoginRequiredMixin, UserPassesTestMixin, SingleTableMixin, FilterView):
    model = RoleRequest
    table_class = RoleRequestTable
    filterset_class = RoleRequestFilter

    @staticmethod
    def post(request, *args, **kwargs):
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

        return HttpResponseRedirect(reverse('roles'))

    def test_func(self):
        return not (Administrator.objects.filter(user=self.request.user) is None)
