def check_empty_spots(formset):
    i = 0
    for form in formset:
        if 'checked' in str(form['DELETE']):
            i += 1
    if len(formset) == 0 or i == len(formset):
        return True


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
