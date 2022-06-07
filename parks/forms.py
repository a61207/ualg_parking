import django_filters
from django import forms
from django.core.exceptions import ValidationError
from .models import Park, Zone, ParkingSpot
import re


class ParkForm(forms.ModelForm):
    monday_start = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    monday_end = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    tuesday_start = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    tuesday_end = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    wednesday_start = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    wednesday_end = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    thursday_start = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    thursday_end = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    friday_start = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    friday_end = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    saturday_start = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    saturday_end = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    sunday_start = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    sunday_end = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    typology = forms.ChoiceField(choices=Park.TYPOLOGYS, widget=forms.Select())
    map_html = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Park
        fields = ("name", "address", "postal_code", "typology", "map_html", "monday_start", "monday_end",
                  "tuesday_start", "tuesday_end", "wednesday_start", "wednesday_end", "thursday_start", "thursday_end",
                  "friday_start", "friday_end", "saturday_start", "saturday_end", "sunday_start", "sunday_end")

    def clean_postal_code(self):
        data = self.cleaned_data['postal_code']
        # noinspection RegExpSimplifiable
        matched = re.match("[0-9]{4}-[0-9]{2}", data)
        if not matched:
            raise ValidationError("Postal Code must have 'xxxx-xxx' format.")
        return data

    def clean_map_html(self):
        data = self.cleaned_data['map_html']
        if not (data.startswith('<iframe src="https://www.google.com/maps/embed?') and data.endswith('"></iframe>')):
            raise ValidationError("Html code must be fully copied.")
        return data

    def clean(self):
        cleaned_data = super(ParkForm, self).clean()

        monday_start = self.cleaned_data['monday_start']
        monday_end = self.cleaned_data['monday_end']
        tuesday_start = self.cleaned_data['tuesday_start']
        tuesday_end = self.cleaned_data['tuesday_end']
        wednesday_start = self.cleaned_data['wednesday_start']
        wednesday_end = self.cleaned_data['wednesday_end']
        thursday_start = self.cleaned_data['thursday_start']
        thursday_end = self.cleaned_data['thursday_end']
        friday_start = self.cleaned_data['friday_start']
        friday_end = self.cleaned_data['friday_end']
        saturday_start = self.cleaned_data['saturday_start']
        saturday_end = self.cleaned_data['saturday_end']
        sunday_start = self.cleaned_data['sunday_start']
        sunday_end = self.cleaned_data['sunday_end']

        if not ((monday_end is None) == (monday_start is None)):
            if monday_end is None:
                raise ValidationError({"monday_end": "End time must be filled."})
            else:
                raise ValidationError({"monday_start": "Start time must be filled."})
        if not ((tuesday_start is None) == (tuesday_end is None)):
            if tuesday_end is None:
                raise ValidationError({"tuesday_end": "End time must be filled."})
            else:
                raise ValidationError({"tuesday_start": "Start time must be filled."})
        if not ((wednesday_start is None) == (wednesday_end is None)):
            if wednesday_end is None:
                raise ValidationError({"wednesday_end": "End time must be filled."})
            else:
                raise ValidationError({"wednesday_start": "Start time must be filled."})
        if not ((thursday_start is None) == (thursday_end is None)):
            if thursday_end is None:
                raise ValidationError({"thursday_end": "End time must be filled."})
            else:
                raise ValidationError({"thursday_start": "Start time must be filled."})
        if not ((friday_start is None) == (friday_end is None)):
            if friday_end is None:
                raise ValidationError({"friday_end": "End time must be filled."})
            else:
                raise ValidationError({"friday_start": "Start time must be filled."})
        if not ((saturday_start is None) == (saturday_end is None)):
            if saturday_end is None:
                raise ValidationError({"saturday_end": "End time must be filled."})
            else:
                raise ValidationError({"saturday_start": "Start time must be filled."})
        if not ((sunday_start is None) == (sunday_end is None)):
            if sunday_end is None:
                raise ValidationError({"sunday_end": "End time must be filled."})
            else:
                raise ValidationError({"sunday_start": "Start time must be filled."})

        return cleaned_data


class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ('name',)


class SpotForm(forms.ModelForm):
    number = forms.IntegerField(widget=forms.HiddenInput())
    x = forms.IntegerField(widget=forms.HiddenInput())
    y = forms.IntegerField(widget=forms.HiddenInput())
    direction = forms.ChoiceField(choices=ParkingSpot.DIRECTIONS, widget=forms.HiddenInput())

    class Meta:
        model = ParkingSpot
        fields = ('number', 'x', 'y', 'direction')
