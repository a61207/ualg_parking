from django.forms.utils import ErrorList
from django.utils import timezone

from main.models import Park, Administrator


def check_empty_spots(formset):
    i = 0
    for form in formset:
        if 'checked' in str(form['DELETE']):
            i += 1
    if len(formset) == 0 or i == len(formset):
        return True


def duplicated_time(form, formset):
    count = -1
    for formP in formset:
        if formP['DELETE'].value() is False and formP['hours'].value() == form['hours'].value() and \
                formP['minutes'].value() == form['minutes'].value() and \
                formP['type'].value() == form['type'].value():
            count += 1
    if count > 0:
        return True
    else:
        return False


def validate_price_type(formset):
    nerrors = 0
    count = 0
    for form in formset:
        if form.is_valid():
            if form['DELETE'].value() is False:
                count += 1
                if form['hours'].value() is '0' and form['minutes'].value() is '0':
                    errors = form.errors.setdefault("__all__", ErrorList())
                    errors.append("Time Values can't have both null values.")
                    nerrors += 1
                elif duplicated_time(form, formset):
                    errors = form.errors.setdefault("__all__", ErrorList())
                    errors.append("Price Type Duration duplicated.")
                    nerrors += 1
    return not nerrors and count != 0


def spot_name_exists(number, spots):
    for spot in spots:
        if spot[3] == number:
            return True
    return False


def spot_overlapped(x, y, direction, spots):
    for spot in spots:
        if spot[2] == "HO" and direction == "HO" and abs(int(spot[0]) - x) <= 1:
            return True
        if spot[2] == "VE" and direction == "VE" and abs(int(spot[1]) - y) <= 1:
            return True
        if spot[2] == "VE" and direction == "HO" and (
                (int(spot[0]) == x and (int(spot[1]) == y or int(spot[1]) + 1 == y)) or
                (int(spot[0]) - 1 == x and (int(spot[1]) == y or int(spot[1]) + 1 == y))):
            return True
    return False


def check_overlaping_spots(formset):
    i = []
    for form in formset:
        if len(form.cleaned_data) == 6 and form.cleaned_data['DELETE'] is False:
            if spot_name_exists(form.cleaned_data['number'], i) or \
                    spot_overlapped(int(form.cleaned_data['x']), int(form.cleaned_data['y']),
                                    form.cleaned_data['direction'], i):
                return True
            i.append([form.cleaned_data['x'], form.cleaned_data['y'], form.cleaned_data['direction'],
                      form.cleaned_data['number']])
    return False


def close_open_park(request):
    if 'close' in request.POST:
        print(Park.objects.filter(id=request.POST['close']).first().is_open)
        Park.objects.filter(id=request.POST['close']).update(is_open=False)
        print(Park.objects.filter(id=request.POST['close']).first().is_open)
    if 'open' in request.POST:
        Park.objects.filter(id=request.POST['open']).update(is_open=True)


def permission_to_update_park_resources(self, resource):
    is_admin = Administrator.objects.filter(user=self.request.user.id).exists()
    if is_admin:
        return (Park.objects.get(id=self.kwargs['park']).reserved_spots(resource.deadline.start_date,
                                                                        resource.deadline.end_date) +
                Park.objects.get(id=self.kwargs['park']).occupied_spots(resource.deadline.start_date,
                                                                        resource.deadline.end_date)) == 0
    return is_admin


def permission_to_archive_park(self):
    return Administrator.objects.filter(user=self.request.user.id).exists() and (
            Park.objects.get(id=self.kwargs['pk']).reserved_spots(timezone.now().date(), timezone.datetime.max) +
            Park.objects.get(id=self.kwargs['pk']).occupied_spots(timezone.now().date(), timezone.datetime.max) == 0 and
            Park.objects.get(id=self.kwargs['pk']).non_achived_resources() == 0)
