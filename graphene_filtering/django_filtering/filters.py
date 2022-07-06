from django_filters import CharFilter, FilterSet

from django_filtering.models import (
    Event,
    Photographer,
    PurchaseOrder,
    PurchaseOrderProduct,
)

# filters.py
...


class PhotographerFilter(FilterSet):
    name = CharFilter()

    class Meta:
        model = Photographer
        fields = {"name": ["exact"]}


class EventFilter(FilterSet):
    photographer__name = CharFilter()

    class Meta:
        model = Event
        fields = "__all__"


class PurchaseOrderFilter(FilterSet):
    class Meta:
        model = PurchaseOrder
        fields = {
            "date": ["gt", "lt", "isnull"],
            "username": ["icontains"],
        }

    products__name = CharFilter(
        lookup_expr="icontains",
    )


class PurchaseOrderProductFilter(FilterSet):
    class Meta:
        model = PurchaseOrderProduct
        fields = {"name": ["icontains"]}
