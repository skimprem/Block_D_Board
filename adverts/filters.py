from django_filters import widgets, FilterSet, DateFromToRangeFilter, RangeFilter, DateFilter
from adverts.models import AdvertFeedback

class FeedbackFilter(FilterSet):
    class Meta:
        model = AdvertFeedback
        fields = [
            'advert'
        ]
        labels = {
            'advert': 'Объявление:'
        }