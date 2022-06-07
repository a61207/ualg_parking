from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.forms import modelformset_factory
from django.forms.utils import ErrorList
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableView, SingleTableMixin

from main.models import Administrator
from parks.forms import ParkForm, ZoneForm, SpotForm, ParkFilter
from parks.functions import check_empty_spots, check_overlaping_spots
from parks.models import Park, Zone, ParkingSpot
from parks.tables import ParkTable, ZoneTable


# Create your views here.
class AddPark(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Park
    form_class = ParkForm

    def test_func(self):
        return not (Administrator.objects.filter(user=self.request.user) is None)

    def form_valid(self, form):
        form.instance.admin = Administrator.objects.get(user=self.request.user)
        return super().form_valid(form)


class ViewParkList(SingleTableMixin, FilterView):
    model = Park
    table_class = ParkTable
    filterset_class = ParkFilter


class ViewParkDetail(DetailView):
    model = Park


class UpdatePark(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Park
    form_class = ParkForm

    def test_func(self):
        return not (Administrator.objects.filter(user=self.request.user) is None)

    def form_valid(self, form):
        form.instance.updated = timezone.now()
        return super().form_valid(form)


class DeletePark(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Park
    success_url = reverse_lazy('list_parks')

    def test_func(self):
        return not (Administrator.objects.filter(user=self.request.user) is None)


class AddZone(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Zone
    form_class = ZoneForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        SpotFormset = modelformset_factory(ParkingSpot, form=SpotForm, extra=0, can_delete=True)
        context['formset'] = SpotFormset(None, queryset=ParkingSpot.objects.none())
        return context

    def test_func(self):
        return not (Administrator.objects.filter(user=self.request.user) is None)

    def form_valid(self, form):
        form.instance.park = Park.objects.get(id=self.kwargs['park'])
        return super().form_valid(form)

    # noinspection PyArgumentList
    def post(self, request, *args, **kwargs):
        form = ZoneForm(request.POST)
        SpotFormSet = modelformset_factory(ParkingSpot, form=SpotForm, extra=0, can_delete=True, can_delete_extra=True)
        formset = SpotFormSet(request.POST)
        if all([form.is_valid(), formset.is_valid()]):
            check_overlaping_spots(formset)
            if check_empty_spots(formset):
                errors = form.errors.setdefault("__all__", ErrorList())
                errors.append("At Least one Spot must be incerted.")
            else:
                parent = form.save(commit=False)
                parent.park = Park.objects.get(id=self.kwargs['park'])
                parent.save()
                for form in formset:
                    if len(form.cleaned_data) == 6 and form.cleaned_data['DELETE'] is False:
                        child = form.save(commit=False)
                        child.zone = parent
                        child.save()
                return HttpResponseRedirect(parent.get_absolute_url())

        return render(request, "parks/zone_form.html", {"form": form, "formset": formset})


class ViewZoneList(SingleTableView):
    model = Zone
    table_class = ZoneTable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['park'] = Park.objects.get(id=self.kwargs['park'])
        return context


class ViewZoneDetail(DetailView):
    model = Zone


class UpdateZone(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Zone
    form_class = ZoneForm

    def test_func(self):
        return not (Administrator.objects.filter(user=self.request.user) is None)

    def form_valid(self, form):
        Park.objects.filter(id=self.kwargs['park']).update(updated=timezone.now())
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        SpotFormset = modelformset_factory(ParkingSpot, form=SpotForm, extra=0, can_delete=True)
        context['formset'] = SpotFormset(None, queryset=ParkingSpot.objects.filter(
            zone=Zone.objects.get(id=self.kwargs['pk'])))
        return context

    # noinspection PyArgumentList
    def post(self, request, *args, **kwargs):
        zone = Zone.objects.get(id=self.kwargs['pk'])
        form = ZoneForm(request.POST, instance=zone)
        SpotFormSet = modelformset_factory(ParkingSpot, form=SpotForm, extra=0, can_delete=True, can_delete_extra=True)
        formset = SpotFormSet(request.POST, queryset=ParkingSpot.objects.filter(
            zone=zone))
        if all([form.is_valid(), formset.is_valid()]):
            if check_empty_spots(formset):
                errors = form.errors.setdefault("__all__", ErrorList())
                errors.append("At Least one Spot must be incerted.")
            else:
                parent = form.save(commit=False)
                parent.park = Park.objects.get(id=self.kwargs['park'])
                parent.save()
                for form in formset:
                    if len(form.cleaned_data) == 6:
                        filterSpot = ParkingSpot.objects.filter(zone=zone, number=form.cleaned_data['number'],
                                                                direction=form.cleaned_data['direction'],
                                                                x=form.cleaned_data['x'], y=form.cleaned_data['y'])
                        if form.cleaned_data['DELETE'] is False:
                            child = form.save(commit=False)
                            child.zone = parent
                            child.save()
                        elif form.cleaned_data['DELETE'] is True and filterSpot is not None:
                            filterSpot.delete()
                return HttpResponseRedirect(parent.get_absolute_url())

        return render(request, "parks/zone_form.html", {"form": form, "formset": formset})


class DeleteZone(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Zone
    success_url = reverse_lazy('list_zones')

    def test_func(self):
        return not (Administrator.objects.filter(user=self.request.user) is None)

    def get_success_url(self):
        return "/parks/" + self.kwargs['park'] + "/zones/"
