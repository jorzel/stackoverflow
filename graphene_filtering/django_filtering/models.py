from django.db import models

# Create your models here.


class Photographer(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)


class Event(models.Model):

    photographer = models.ForeignKey(
        Photographer,
        on_delete=models.SET_NULL,
        null=True,
        related_name="event_photographer",
    )


class PurchaseOrder(models.Model):
    username = models.CharField(max_length=100)
    date = models.DateField()


class PurchaseOrderProduct(models.Model):
    name = models.CharField(max_length=200)
    order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products",
    )
