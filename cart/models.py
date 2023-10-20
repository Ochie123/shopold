from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Count, Sum

from accounts.models import User
from products.models import Product
# Create your models here.
import logging
logger = logging.getLogger(__name__)

class Cart(models.Model):
    OPEN = 10
    SUBMITTED = 20
    STATUSES = ((OPEN, "Open"), (SUBMITTED, "Submitted"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    status = models.IntegerField(choices=STATUSES, default=OPEN)

    def is_empty(self):
        return self.cartline_set.all().count() == 0

    def count(self):
        return sum(i.quantity for i in self.cartline_set.all())

class CartLine(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) 
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE )
    quantity = models.PositiveIntegerField( default=1, validators=[MinValueValidator(1)]
)
