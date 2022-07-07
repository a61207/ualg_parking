from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.safestring import mark_safe

from main.models import Park, Zone, ParkingSpot, PriceType, TimePeriod, DatePeriod
import re

from main.static import postal_codes


class ParkForm(forms.ModelForm):
    typology = forms.ChoiceField(choices=Park.TYPOLOGYS, widget=forms.Select())
    map_html = forms.CharField(widget=forms.TextInput(), help_text=mark_safe("Search address in <a "
                                                                             "href='https://www.google.pt/maps/' "
                                                                             "target='_blank'>Google Maps</a>, select "
                                                                             "<b>Share</b> and <b>Embed Maps</b> "
                                                                             "buttons and then copy and paste the Html "
                                                                             "code."))

    class Meta:
        model = Park
        fields = ("name", "address", "postal_code", "typology", "map_html")

    def clean_postal_code(self):
        data = self.cleaned_data['postal_code']
        # noinspection RegExpSimplifiable
        matched = re.match("[0-9]{4}-[0-9]{2}", data)
        if not matched:
            raise ValidationError("Postal Code must have 'xxxx-xxx' format.")
        count = 0
        for x in postal_codes.CITY:
            if x[0] == data[:2]:
                count += 1
        if count == 0:
            raise ValidationError("Postal Code does not exists.")
        return data

    def clean_map_html(self):
        data = self.cleaned_data['map_html']
        if not (data.startswith('<iframe src="https://www.google.com/maps/embed?') and data.endswith('"></iframe>')):
            raise ValidationError("Html code must be fully copied.")
        return data

    def clean(self):
        cleaned_data = super(ParkForm, self).clean()
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


class PriceTypeForm(forms.ModelForm):

    minutes = forms.IntegerField(required=True, initial=0, min_value=0, max_value=59,
                                 widget=forms.NumberInput(attrs={'value': 0}))
    hours = forms.IntegerField(required=True, initial=0, min_value=0, widget=forms.NumberInput(attrs={'value': 0}))
    total = forms.DecimalField(label="Total Cost", required=True, initial=0, min_value=0, decimal_places=2,
                               max_digits=14, widget=forms.NumberInput(attrs={'value': 0}))
    type = forms.ChoiceField(required=True, choices=PriceType.TYPE, initial=PriceType.NORMAL)

    class Meta:
        model = PriceType
        fields = ('hours', 'minutes', 'total', 'type')


class TimePeriodForm(forms.ModelForm):
    check = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    start = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}), required=False)
    end = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}), required=False)

    class Meta:
        model = TimePeriod
        fields = ('start', 'end')

    def clean(self):
        cleaned_data = super(TimePeriodForm, self).clean()
        if self.cleaned_data['start'] is not None and self.cleaned_data['end'] is not None:
            time1 = self.cleaned_data['start']
            time2 = self.cleaned_data['end']
            if time1 >= time2:
                raise ValidationError("Invalid Schedule")
        return cleaned_data


class DatePeriodForm(forms.ModelForm):
    date1 = timezone.now()
    date2 = timezone.now()
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',
                                                               'min': date1.date()}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',
                                                             'min': date2.date()}))

    class Meta:
        model = DatePeriod
        fields = ('start_date', 'end_date')
