import django_filters
from .models import *
from django.db.models import FloatField, F, Value ,ExpressionWrapper
from django.db.models.functions import Cast
from haversine import haversine, Unit
import math
from django.db.models.expressions import RawSQL
from math import radians


class MaydonFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(method='filter_by_time', label='Start Time')
    end_time = django_filters.DateTimeFilter(method='filter_by_time', label='End Time')
    latitude = django_filters.NumberFilter(method='filter_by_location', label='Latitude')
    longitude = django_filters.NumberFilter(method='filter_by_location', label='Longitude')

    class Meta:
        model = Maydon
        fields = ['start_time', 'end_time', 'latitude', 'longitude']

    def filter_by_time(self, queryset, name, value):
        start_time = self.data.get('start_time')
        end_time = self.data.get('end_time')
        if not start_time or not end_time:
            raise django_filters.exceptions.ValidationError("Boshlanish va Tugash vaqtlari kerak")
        booked_fields = Bron.objects.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            is_active=True
        ).values_list('maydon_id', flat=True)
        return queryset.exclude(id__in=booked_fields)

    def filter_by_location(self, queryset, name, value):
        user_latitude = float(self.data.get('latitude'))
        user_longitude = float(self.data.get('longitude'))
        R = 6371
        user_lat_radians = radians(user_latitude)
        user_lon_radians = radians(user_longitude)

        haversine_formula = """
            %s * acos(
                cos(radians(%s)) * cos(radians(latitude)) * 
                cos(radians(longitude) - radians(%s)) + 
                sin(radians(%s)) * sin(radians(latitude))
            )
        """ % (R, user_latitude, user_longitude, user_latitude)

        queryset = queryset.annotate(
            distance=RawSQL(haversine_formula, [], output_field=FloatField())
        ).order_by('distance')

        return queryset

