from django.db import models
from django.db.models import ForeignKey


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Product Name")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Category'
    )
    description = models.TextField(verbose_name="Product Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    is_available = models.BooleanField(default=True, verbose_name="Is Available")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

class Review(models.Model):
    product = ForeignKey(Product, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField()

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"