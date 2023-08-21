import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class OrderFilter(django_filters.FilterSet):

	start_date = DateFilter(field_name="date_created", lookup_expr='gte')  #these are the custom filters
	end_date = DateFilter(field_name="date_created", lookup_expr='lte')

	note = CharFilter(field_name='note', lookup_expr='icontains')  #icontains means ignore case sensitivity

	class Meta:
		model = Order
		fields = '__all__'  #adds all fields from Order
		exclude = ['customer', 'date_created'] #excludes these two fields

