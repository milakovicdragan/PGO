import django_filters
from django.forms import DateInput, TimeInput
from bootstrap_datepicker_plus.widgets import DatePickerInput, DateTimePickerInput,TimePickerInput
#from bootstrap_datepicker_plus.widgets import DateInput
from slikeRadar.models import Slike

class SlikeFilter(django_filters.FilterSet):
    time_create = django_filters.TimeFilter(widget=TimeInput())
    class Meta:
        model = Slike
        fields = ["time_create"]


