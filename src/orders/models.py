from django.db import models
from course.models import Course
from xarala.utils import generate_key


class Order(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    invoice_number = models.CharField(max_length=10, null=True, blank=True, unique=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)

    def _get_unique_invoice_number(self):
        unique_invoice_number = f"FCT_{generate_key()}"
        while Order.objects.filter(invoice_number=unique_invoice_number).exists():
            unique_invoice_number = f"FCT_{generate_key()}"
        return unique_invoice_number

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self._get_unique_invoice_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity