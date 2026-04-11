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
    rating = models.IntegerField(blank=True, null=True)

# ================================================


# korzyna, zberigaetsa inforamjca v brauzere
class CartItem(models.Model):
    # session_key - kluch sessii brauzera
    session_key = models.CharField(
        max_length=50,
        verbose_name="Session key"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Item"
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Items quantity"
    )

    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Added at"
    )

    class Meta:
        verbose_name="Cart item"
        verbose_name_plural="Cart"
        unique_together=["session_key", "product"]

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'  # potato x4

    @property
    def total_price(self):
        """Price of this item (price * quantity)"""
        return self.product.price * self.quantity

# zakaz
# nomer zakaza i informacja pro pokupcya
# sozdayetsa posle potverzhdenia oplaty
class Order(models.Model):
    product_list = []
    order_number = models.CharField(max_length=50, unique=True, verbose_name='Order number')
    customer_name = models.CharField(max_length=200, verbose_name='Customer name')
    customer_email = models.EmailField(max_length=100, verbose_name='Customer email')
    customer_phone = models.CharField(max_length=20, blank=True, verbose_name='Customer phone')


# tovary v zakaze
# schto i v kakom kolichestve zakazano
class OrderItem(models.Model):
    pass
