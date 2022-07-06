import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from django_filtering.filters import (
    EventFilter,
    PhotographerFilter,
    PurchaseOrderFilter,
    PurchaseOrderProductFilter,
)
from django_filtering.models import (
    Event,
    Photographer,
    PurchaseOrder,
    PurchaseOrderProduct,
)


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        interfaces = (graphene.relay.Node,)
        filterset_class = EventFilter


class PhotographerType(DjangoObjectType):
    class Meta:
        model = Photographer
        filterset_class = PhotographerFilter
        interfaces = (graphene.relay.Node,)


class PurchasesOrderProduct(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)

    class Meta:
        model = PurchaseOrderProduct
        interfaces = (graphene.relay.Node,)
        filterset_class = PurchaseOrderProductFilter


class Purchases(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)
    products = DjangoFilterConnectionField(PurchasesOrderProduct)

    class Meta:
        model = PurchaseOrder
        interfaces = (graphene.relay.Node,)
        filterset_class = PurchaseOrderFilter

    @staticmethod
    def resolve_products(self, info, **kwargs):
        return (
            PurchaseOrderProduct.objects.filter(order_id=self.id).order_by("name").all()
        )


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    events = DjangoFilterConnectionField(EventType, filterset_class=EventFilter)

    purchases = DjangoFilterConnectionField(Purchases)

    @staticmethod
    def resolve_purchases(self, info, date_filter=None, **kwargs):
        return PurchaseOrder.objects.all().order_by("-date")


schema = graphene.Schema(query=Query)
