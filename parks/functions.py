from django.forms.utils import ErrorList


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
        if formP.cleaned_data['DELETE'] is False and formP.cleaned_data['hours'] == form.cleaned_data['hours'] and \
                formP.cleaned_data['minutes'] == form.cleaned_data['minutes']:
            count += 1
    if count > 0:
        return True
    else:
        return False


def duplicated_contract(form, formset):
    count = -1
    for formP in formset:
        if formP.cleaned_data['DELETE'] is False and formP.cleaned_data['years'] == form.cleaned_data['years'] and \
                formP.cleaned_data['months'] == form.cleaned_data['months'] and \
                formP.cleaned_data['name'] == form.cleaned_data['name']:
            count += 1
    if count > 0:
        return True
    else:
        return False


def validate_price_type(formset):
    nerrors = 0
    count = 0
    for form in formset:
        if form.is_valid() and form.cleaned_data:
            if form.cleaned_data and form.cleaned_data['DELETE'] is False:
                count += 1
                if form.cleaned_data['hours'] == 0 and form.cleaned_data['minutes'] == 0:
                    errors = form.errors.setdefault("__all__", ErrorList())
                    errors.append("Time Values can't have null values.")
                    nerrors += 1
                elif duplicated_time(form, formset):
                    errors = form.errors.setdefault("__all__", ErrorList())
                    errors.append("Price Type Duration already defined.")
                    nerrors += 1
    return not nerrors and count != 0


def validate_contract_type(formset):
    nerrors = 0
    count = 0
    for form in formset:
        if form.is_valid() and form.cleaned_data:
            if form.cleaned_data and form.cleaned_data['DELETE'] is False:
                count += 1
                if form.cleaned_data['years'] == 0 and form.cleaned_data['months'] == 0 \
                        and not form.cleaned_data['name']:
                    errors = form.errors.setdefault("__all__", ErrorList())
                    errors.append("Time Values can't have null values.")
                    nerrors += 1
                elif duplicated_contract(form, formset):
                    errors = form.errors.setdefault("__all__", ErrorList())
                    errors.append("Contract Type Duration and name already defined.")
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
