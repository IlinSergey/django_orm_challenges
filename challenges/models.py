from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=256)
    author_full_name = models.CharField(max_length=256)
    isbn = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Laptop(models.Model):
    BRAND_CHOICES = [
        ('apple', 'Apple'),
        ('asus', 'Asus'),
        ('hp', 'HP'),
        ('lenovo', 'Lenovo'),
    ]
    brand = models.CharField(max_length=6, choices=BRAND_CHOICES)
    year = models.PositiveSmallIntegerField()
    ram = models.PositiveSmallIntegerField()
    hdd = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brand

    def to_json(self):
        """
        Returns a JSON representation of the object with the following attributes:
        brand, year, ram, hdd, price, and quantity.
        """
        return {
            'brand': self.brand,
            'year': self.year,
            'ram': self.ram,
            'hdd': self.hdd,
            'price': self.price,
            'quantity': self.quantity,
        }

    class Meta:
        ordering = ['brand']
        indexes = [
            models.Index(fields=['brand']),
        ]
        verbose_name = 'Ноутбук'
        verbose_name_plural = 'Ноутбуки'
