import factory

from django_filtering.models import (
    Event,
    Photographer,
    PurchaseOrder,
    PurchaseOrderProduct,
)


class PhotographerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photographer

    email = "x@wp.pl"
    name = "Super fast zipper"


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    photographer = factory.SubFactory(PhotographerFactory)


class PurchaseOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PurchaseOrder

    date = "2021-01-01"


class PurchaseOrderProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PurchaseOrderProduct

    name = "xxx"
    order = factory.SubFactory(PurchaseOrderFactory)
