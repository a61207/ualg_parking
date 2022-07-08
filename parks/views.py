from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import modelformset_factory
from django.forms.utils import ErrorList
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from main.models import *
from main.static import postal_codes
from parks.filters import ParkFilter, ZoneFilter, WeekScheduleFilter, PriceTableFilter
from parks.forms import ParkForm, ZoneForm, SpotForm, PriceTypeForm, TimePeriodForm, DatePeriodForm
from parks.functions import check_empty_spots, check_overlaping_spots, validate_price_type, close_open_park, \
    permission_to_update_park_resources, permission_to_archive_park, close_open_zone, permission_to_archive_zone, \
    permission_to_archive_spot
from parks.tables import ParkTable, ZoneTable, WeekScheduleTable, ClientParkTable, PriceTableTable, ClientZoneTable


# Create your views here.
class AddPark(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Park
    form_class = ParkForm
    template_name = 'parks/park_add.html'
    success_message = "Park was created successfully"

    def test_func(self):
        return Administrator.objects.filter(user=self.request.user.id).exists()

    def form_valid(self, form):
        form.instance.admin = Administrator.objects.get(user=self.request.user)
        for x in postal_codes.CITY:
            if x[0] == form.instance.postal_code[:2]:
                form.instance.city = x[1]
        return super().form_valid(form)


class AddWeekDaySchedule(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'schedule/weekschedule_add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['park_id'] = kwargs['pk']
        context['deadline'] = DatePeriodForm(auto_id="deadline_%s")
        TimePeriodFormset = modelformset_factory(TimePeriod, form=TimePeriodForm, extra=7)
        context['formset'] = TimePeriodFormset(None, queryset=TimePeriod.objects.none())
        return context

    def test_func(self):
        return Administrator.objects.filter(user=self.request.user.id).exists()

    @staticmethod
    def post(request, *args, **kwargs):
        deadlineform = DatePeriodForm(request.POST, auto_id="deadline_%s")
        TimePeriodFormset = modelformset_factory(TimePeriod, form=TimePeriodForm, extra=0)
        formset = TimePeriodFormset(request.POST)
        if deadlineform.is_valid() and formset.is_valid():
            count = 0
            errors = 0
            times = [0] * len(formset)
            for x in range(len(formset)):
                if 'start' in formset[x].cleaned_data and 'end' in formset[x].cleaned_data:
                    count += 1
            for schedule in WeekSchedule.objects.filter(archived=False, park=kwargs['pk']):
                if schedule.deadline.start_date <= deadlineform.cleaned_data['start_date'] <= \
                        schedule.deadline.end_date or \
                        schedule.deadline.end_date >= deadlineform.cleaned_data['end_date'] >= \
                        schedule.deadline.start_date:
                    errors += 1
                    errors = deadlineform.errors.setdefault("__all__", ErrorList())
                    errors.append("Choosen deadline already in a schedule from " +
                                  schedule.deadline.start_date.strftime("%d/%m/%Y") +
                                  " to " + schedule.deadline.end_date.strftime("%d/%m/%Y") + " .")
            if count == 0:
                errors = deadlineform.errors.setdefault("__all__", ErrorList())
                errors.append("Must choose one of the week days option.")
            elif errors == 0:
                deadline = deadlineform.save()
                for x in range(len(formset)):
                    if 'start' in formset[x].cleaned_data and 'end' in formset[x].cleaned_data:
                        times[x] = TimePeriod.objects.create(start=formset[x].cleaned_data['start'],
                                                             end=formset[x].cleaned_data['end'])
                    else:
                        times[x] = TimePeriod.objects.create(start=None, end=None)
                WeekSchedule.objects.create(deadline=deadline, monday=times[0], tuesday=times[1],
                                            wednesday=times[2], thursday=times[3], friday=times[4],
                                            saturday=times[5], sunday=times[6],
                                            park=Park.objects.get(id=kwargs['pk']))
                return HttpResponseRedirect(reverse('list_schedules', kwargs={'pk': kwargs['pk']}))
        return render(request, "schedule/weekschedule_add.html", {"deadline": deadlineform, "formset": formset,
                                                                  "park_id": kwargs['pk']})


# noinspection PyArgumentList,PyUnresolvedReferences
class AddPriceTable(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PriceType
    form_class = PriceTypeForm
    template_name = 'price/price_type_add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deadline'] = DatePeriodForm(auto_id="deadline_%s")
        context['park_id'] = self.kwargs['pk']
        PriceTypeFormset = modelformset_factory(PriceType, form=PriceTypeForm, extra=1, can_delete_extra=True,
                                                can_delete=True)
        context['formset'] = PriceTypeFormset(None, queryset=PriceType.objects.none())
        return context

    def test_func(self):
        return Administrator.objects.filter(user=self.request.user.id).exists()

    def post(self, request, *args, **kwargs):
        deadlineform = DatePeriodForm(request.POST, auto_id="deadline_%s")
        PriceTypeFormset = modelformset_factory(PriceType, form=PriceTypeForm, extra=0, can_delete=True,
                                                can_delete_extra=True)
        formset = PriceTypeFormset(request.POST)
        if deadlineform.is_valid() and formset.is_valid():
            park = Park.objects.get(id=self.kwargs['pk'])
            # noinspection DuplicatedCode
            errors = 0
            for table in PriceTable.objects.filter(archived=False, park=kwargs['pk']):
                if table.deadline.start_date <= deadlineform.cleaned_data['start_date'] <= \
                        table.deadline.end_date or \
                        table.deadline.end_date >= deadlineform.cleaned_data['end_date'] >= \
                        table.deadline.start_date:
                    errors += 1
                    errors = deadlineform.errors.setdefault("__all__", ErrorList())
                    errors.append("Choosen deadline already in a price table from " +
                                  table.deadline.start_date.strftime("%d/%m/%Y") +
                                  " to " + table.deadline.end_date.strftime("%d/%m/%Y") + " .")

            count = 0
            for form in formset:
                if form.is_valid():
                    if form['DELETE'].value() is False:
                        count += 1
            if validate_price_type(formset) and errors == 0:
                deadline = deadlineform.save()
                table = PriceTable.objects.create(park=park, deadline=deadline)
                for form in formset:
                    if form['DELETE'].value() is False:
                        total = form['total'].value()
                        minutes = form['minutes'].value()
                        hours = form['hours'].value()
                        ttype = form['type'].value()
                        PriceType.objects.create(table=table, total=total, minutes=minutes, hours=hours, type=ttype)
                return HttpResponseRedirect(reverse('list_prices', kwargs={'pk': park.id}))
            elif count == 0:
                errors = deadlineform.errors.setdefault("__all__", ErrorList())
                errors.append("Must have at least one price type.")
        return render(request, "price/price_type_add.html", {"deadline": deadlineform, "formset": formset,
                                                             "park_id": self.kwargs['pk']})


class ViewParkList(SingleTableMixin, FilterView):
    model = Park
    table_class = ClientParkTable
    filterset_class = ParkFilter
    template_name = 'parks/park_filter.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated and Administrator.objects.filter(user=self.request.user):
            return qs
        else:
            return qs.filter(is_archived=False)

    def get_table_class(self):
        if self.request.user.is_authenticated and Administrator.objects.filter(user=self.request.user):
            return ParkTable
        else:
            return self.table_class

    @staticmethod
    def post(request, *args, **kwargs):
        if Administrator.objects.filter(user=request.user.id).exists():
            close_open_park(request)
        return HttpResponseRedirect(reverse('list_parks'))


class ViewWeekDayScheduleList(LoginRequiredMixin, UserPassesTestMixin, SingleTableMixin, FilterView):
    model = WeekSchedule
    table_class = WeekScheduleTable
    filterset_class = WeekScheduleFilter
    template_name = 'schedule/weekschedule_filter.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(park=Park.objects.get(id=self.kwargs['pk'])) \
            .order_by('archived', 'deadline__start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['park'] = Park.objects.get(id=self.kwargs['pk'])
        return context

    def test_func(self):
        return Administrator.objects.filter(user=self.request.user.id).exists()


class ViewPriceTableList(LoginRequiredMixin, UserPassesTestMixin, SingleTableMixin, FilterView):
    model = PriceTable
    table_class = PriceTableTable
    filterset_class = PriceTableFilter
    template_name = 'price/pricetable_filter.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(park=Park.objects.get(id=self.kwargs['pk'])) \
            .order_by('archived', 'deadline__start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['park'] = Park.objects.get(id=self.kwargs['pk'])
        return context

    def test_func(self):
        return Administrator.objects.filter(user=self.request.user.id).exists()


class ViewParkDetail(DetailView):
    model = Park
    template_name = 'parks/park_detail.html'

    @staticmethod
    def post(request, *args, **kwargs):
        if Administrator.objects.filter(user=request.user.id).exists():
            close_open_park(request)
        return HttpResponseRedirect(reverse('park_detail', kwargs={'pk': kwargs['pk']}))


class UpdatePark(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Park
    form_class = ParkForm
    template_name = 'parks/park_update.html'

    def test_func(self):
        return Administrator.objects.filter(user=self.request.user.id).exists()

    def form_valid(self, form):
        form.instance.updated = timezone.now()
        for x in postal_codes.CITY:
            if x[0] == form.cleaned_data['postal_code'][:2]:
                form.instance.city = x[1]
        return super().form_valid(form)


class UpdateWeekDaySchedule(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'schedule/weekschedule_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule = WeekSchedule.objects.get(id=kwargs['pk'])
        context['park_id'] = kwargs['park']
        context['deadline'] = DatePeriodForm(auto_id="deadline_%s",
                                             instance=DatePeriod.objects.get(weekschedule=schedule))
        TimePeriodFormset = modelformset_factory(TimePeriod, form=TimePeriodForm, extra=0)
        context['formset'] = TimePeriodFormset(None, queryset=schedule.get_time_days())
        return context

    def test_func(self):
        schedule = WeekSchedule.objects.get(id=self.kwargs['pk'])
        return permission_to_update_park_resources(self, schedule)

    @staticmethod
    def post(request, *args, **kwargs):
        schedule = WeekSchedule.objects.get(id=kwargs['pk'])
        deadlineform = DatePeriodForm(request.POST, auto_id="deadline_%s",
                                      instance=DatePeriod.objects.get(weekschedule=schedule))
        TimePeriodFormset = modelformset_factory(TimePeriod, form=TimePeriodForm, extra=0)
        formset = TimePeriodFormset(request.POST, queryset=schedule.get_time_days())
        if deadlineform.is_valid() and formset.is_valid():
            count = 0
            errors = 0
            for x in range(len(formset)):
                if 'start' in formset[x].cleaned_data and 'end' in formset[x].cleaned_data:
                    count += 1
            for schedule in WeekSchedule.objects.filter(archived=False, park=kwargs['park']):
                if (schedule.deadline.start_date <= deadlineform.cleaned_data['start_date'] <=
                    schedule.deadline.end_date or schedule.deadline.end_date >=
                    deadlineform.cleaned_data['end_date'] >= schedule.deadline.start_date) and \
                        schedule.id != kwargs['pk']:
                    errors += 1
                    error = deadlineform.errors.setdefault("__all__", ErrorList())
                    error.append("Choosen deadline already in a schedule from " +
                                 schedule.deadline.start_date.strftime("%d/%m/%Y") +
                                 " to " + schedule.deadline.end_date.strftime("%d/%m/%Y") + " .")
            if count == 0:
                error = deadlineform.errors.setdefault("__all__", ErrorList())
                error.append("Must choose one of the week days option.")
            elif errors == 0:
                deadlineform.save()
                formset.save()
                return HttpResponseRedirect(reverse('list_schedules', kwargs={'pk': kwargs['park']}))
        return render(request, "schedule/weekschedule_update.html", {"deadline": deadlineform, "formset": formset,
                                                                     "park_id": kwargs['park']})


# noinspection PyUnresolvedReferences,PyArgumentList
class UpdatePriceType(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PriceTable
    form_class = PriceTypeForm
    template_name = 'price/price_type_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        price = PriceTable.objects.get(id=self.kwargs['pk'])
        context['park_id'] = self.kwargs['park']
        context['deadline'] = DatePeriodForm(auto_id="deadline_%s",
                                             instance=DatePeriod.objects.get(pricetable=price))
        PriceTypeFormset = modelformset_factory(PriceType, form=PriceTypeForm, extra=0, can_delete_extra=True,
                                                can_delete=True)
        context['formset'] = PriceTypeFormset(None, queryset=price.get_prices())
        return context

    def test_func(self):
        price = PriceTable.objects.get(id=self.kwargs['pk'])
        return permission_to_update_park_resources(self, price)

    def post(self, request, *args, **kwargs):
        price = PriceTable.objects.get(id=self.kwargs['pk'])
        deadlineform = DatePeriodForm(request.POST, auto_id="deadline_%s",
                                      instance=DatePeriod.objects.get(pricetable=price))
        PriceTypeFormset = modelformset_factory(PriceType, form=PriceTypeForm, extra=0, can_delete=True,
                                                can_delete_extra=True)
        park = Park.objects.get(id=self.kwargs['park'])
        formset = PriceTypeFormset(request.POST)
        if deadlineform.is_valid() and formset.is_valid():
            # noinspection DuplicatedCode
            errors = 0
            for table in PriceTable.objects.filter(archived=False, park=kwargs['park']):
                if (table.deadline.start_date <= deadlineform.cleaned_data['start_date'] <=
                    table.deadline.end_date or
                    table.deadline.end_date >= deadlineform.cleaned_data['end_date'] >=
                    table.deadline.start_date) and \
                        table.id != kwargs['pk']:
                    errors += 1
                    errors = deadlineform.errors.setdefault("__all__", ErrorList())
                    errors.append("Choosen deadline already in a price table from " +
                                  table.deadline.start_date.strftime("%d/%m/%Y") +
                                  " to " + table.deadline.end_date.strftime("%d/%m/%Y") + " .")
            count = 0
            for form in formset:
                if form.is_valid():
                    if form['DELETE'].value() is False:
                        count += 1
            if validate_price_type(formset) and errors == 0:
                deadlineform.save()
                for form in formset:
                    filterType = PriceType.objects.filter(table=price, total=form.cleaned_data['total'],
                                                          minutes=form.cleaned_data['minutes'],
                                                          hours=form.cleaned_data['hours'],
                                                          type=form.cleaned_data['type'])
                    if form.cleaned_data['DELETE'] is False:
                        child = form.save(commit=False)
                        child.table = price
                        child.save()
                    elif form.cleaned_data['DELETE'] is True and filterType is not None:
                        filterType.delete()
                return HttpResponseRedirect(reverse('list_prices', kwargs={'pk': park.id}))
            elif count == 0:
                errors = deadlineform.errors.setdefault("__all__", ErrorList())
                errors.append("Must have at least one price type.")
        return render(request, "price/price_type_update.html", {"deadline": deadlineform, "formset": formset,
                                                                "park_id": park.id})


class ArchivePark(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'parks/park_confirm_archive.html'

    def test_func(self):
        return permission_to_archive_park(self)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Park.objects.get(id=kwargs['pk'])
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        Park.objects.filter(id=kwargs['pk']).update(is_archived=True, is_open=False)
        for zone in Park.objects.get(id=kwargs['pk']).zones():
            Zone.objects.filter(id=zone.id).update(is_archived=True, is_open=False)
            for spot in Zone.objects.get(id=zone.id).spots():
                ParkingSpot.objects.filter(id=spot.id).update(is_archived=True)
        return HttpResponseRedirect(reverse('park_detail', kwargs={'pk': kwargs['pk']}))


class ArquiveSchedule(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'schedule/weekschedule_confirm_arquive.html'

    def test_func(self):
        schedule = WeekSchedule.objects.get(id=self.kwargs['pk'])
        return permission_to_update_park_resources(self, schedule)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule_id'] = kwargs['pk']
        context['park_id'] = kwargs['park']
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        WeekSchedule.objects.filter(id=kwargs['pk']).update(archived=True)
        return HttpResponseRedirect(reverse('list_schedules', kwargs={'pk': kwargs['park']}))


class ArquivePriceTable(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'price/pricetable_confirm_arquive.html'

    def test_func(self):
        price = PriceTable.objects.get(id=self.kwargs['pk'])
        return permission_to_update_park_resources(self, price)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = kwargs['pk']
        context['park_id'] = kwargs['park']
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        PriceTable.objects.filter(id=kwargs['pk']).update(archived=True)
        return HttpResponseRedirect(reverse('list_prices', kwargs={'pk': kwargs['park']}))


class AddZone(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Zone
    form_class = ZoneForm
    template_name = 'zone/zone_add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        SpotFormset = modelformset_factory(ParkingSpot, form=SpotForm, extra=0, can_delete=True)
        context['formset'] = SpotFormset(None, queryset=ParkingSpot.objects.none())
        context['park'] = Park.objects.get(id=self.kwargs['park'])
        return context

    def test_func(self):
        return Administrator.objects.filter(user=self.request.user.id).exists()

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
            elif Zone.objects.filter(park=Park.objects.get(id=self.kwargs['park']),
                                     name=form.cleaned_data['name']).exists():
                errors = form.errors.setdefault("__all__", ErrorList())
                errors.append("Name Zone already exists.")
            else:
                parent = form.save(commit=False)
                parent.park = Park.objects.get(id=self.kwargs['park'])
                parent.save()
                for form in formset:
                    if len(form.cleaned_data) == 6 and form.cleaned_data['DELETE'] is False:
                        child = form.save(commit=False)
                        child.zone = parent
                        child.save()
                zone = Zone.objects.last()
                return HttpResponseRedirect(reverse('zone_detail', kwargs={'park': zone.park.id, 'pk': zone.id}))
        print(formset.errors)
        print(request.POST)
        return render(request, "zone/zone_add.html", {"form": form, "formset": formset,
                                                      "park": Park.objects.get(id=kwargs['park'])})


class ViewZoneList(SingleTableMixin, FilterView):
    model = Zone
    table_class = ClientZoneTable
    filterset_class = ZoneFilter
    template_name = 'zone/zone_filter.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated and Administrator.objects.filter(user=self.request.user):
            return qs.filter(park=Park.objects.get(id=self.kwargs['park']))
        else:
            return qs.filter(is_archived=False, park=Park.objects.get(id=self.kwargs['park']))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['park'] = Park.objects.get(id=self.kwargs['park'])
        return context

    def get_table_class(self):
        if self.request.user.is_authenticated and Administrator.objects.filter(user=self.request.user):
            return ZoneTable
        else:
            return self.table_class

    @staticmethod
    def post(request, *args, **kwargs):
        if Administrator.objects.filter(user=request.user.id).exists():
            close_open_zone(request)
        return HttpResponseRedirect(reverse('list_zones', kwargs={'park': kwargs['park']}))


class ViewZoneDetail(DetailView):
    model = Zone
    template_name = 'zone/zone_detail.html'

    @staticmethod
    def post(request, *args, **kwargs):
        if Administrator.objects.filter(user=request.user.id).exists():
            close_open_zone(request)
        return HttpResponseRedirect(reverse('zone_detail', kwargs={'park': kwargs['park'], 'pk': kwargs['pk']}))


class UpdateZone(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Zone
    form_class = ZoneForm
    template_name = 'zone/zone_update.html'

    def test_func(self):
        return Administrator.objects.filter(user=self.request.user.id).exists()

    def form_valid(self, form):
        Park.objects.filter(id=self.kwargs['park']).update(updated=timezone.now())
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        SpotFormset = modelformset_factory(ParkingSpot, form=SpotForm, extra=0, can_delete=True)
        context['formset'] = SpotFormset(None, queryset=ParkingSpot.objects.filter(
            zone=Zone.objects.get(id=self.kwargs['pk']), is_archived=False))
        context['zone'] = Zone.objects.get(id=self.kwargs['pk'])
        return context

    # noinspection PyArgumentList
    def post(self, request, *args, **kwargs):
        zone = Zone.objects.get(id=self.kwargs['pk'])
        form = ZoneForm(request.POST, instance=zone)
        SpotFormSet = modelformset_factory(ParkingSpot, form=SpotForm, extra=0, can_delete=True, can_delete_extra=True)
        formset = SpotFormSet(request.POST, queryset=ParkingSpot.objects.filter(
            zone=zone, is_archived=False))
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
                                                                x=form.cleaned_data['x'], y=form.cleaned_data['y'],
                                                                is_archived=False)
                        if form.cleaned_data['DELETE'] is False:
                            child = form.save(commit=False)
                            child.zone = parent
                            child.save()
                        elif form.cleaned_data['DELETE'] is True and filterSpot is not None:
                            filterSpot.update(is_archived=True)
                return HttpResponseRedirect(parent.get_absolute_url())

        return render(request, "zone/zone_update.html", {"form": form, "formset": formset, "zone": zone})


class ArchiveZone(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'zone/zone_confirm_archive.html'

    def test_func(self):
        return permission_to_archive_zone(self)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Zone.objects.get(id=kwargs['pk'])
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        Zone.objects.filter(id=kwargs['pk']).update(is_archived=True, is_open=False)
        for spot in Zone.objects.get(id=kwargs['pk']).spots():
            ParkingSpot.objects.filter(id=spot.id).update(is_archived=True)
        return HttpResponseRedirect(reverse('zone_detail', kwargs={'park': kwargs['park'], 'pk': kwargs['pk']}))


class ArchiveSpot(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'zone/spot_confirm_archive.html'

    def test_func(self):
        return permission_to_archive_spot(self)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = ParkingSpot.objects.get(id=kwargs['pk'])
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        ParkingSpot.objects.filter(id=kwargs['pk']).update(is_archived=True)
        return HttpResponseRedirect(reverse('zone_detail', kwargs={'park': kwargs['park'], 'pk': kwargs['zone']}))

