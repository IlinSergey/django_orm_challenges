from django.db import models
from django.utils import timezone


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


"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст,
имя автора, статус (опубликован/не опубликован/забанен), дата создания, дата публикации,
категория (одна из нескольких вариантов).
"""


class Post(models.Model):

    STATUS_CHOICES = [
        ('published', 'Опубликован'),
        ('draft', 'Не опубликован'),
        ('ban', 'Забанен'),
    ]
    CATEGORY_CHOICES = [
        ('news', 'Новости'),
        ('travel', 'Путешествия'),
        ('food', 'Еда'),
        ('music', 'Музыка'),
        ('sport', 'Спорт'),
    ]
    title = models.CharField(max_length=256)
    text = models.CharField(max_length=5000)
    author = models.CharField(max_length=30)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, default=None, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == 'published':
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def to_json(self):
        """
        Returns a JSON representation of the object with the following attributes:
        title, text, author, status, category.
        """
        return {
            'id': self.pk,
            'title': self.title,
            'text': self.text,
            'author': self.author,
            'status': self.status,
            'category': self.category,
        }

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
