from django_filters import FilterSet
from typing import Type
from django.db.models import Model


def filter_factory(filter_model: Type[Model], filter_fields: list[str]):
    class NewFilter(FilterSet):
        class Meta:
            model = filter_model
            fields = filter_fields

    return NewFilter
