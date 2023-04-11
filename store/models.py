from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    summery = models.TextField(blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    sku = models.IntegerField(blank=True)
    available = models.BooleanField(default=True)
    tag = models.ManyToManyField('Tag')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

class Image(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='product', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    email = models.EmailField()
    review = models.TextField()
    created = models.DateTimeField()

    def __str__(self):
        return self.product.name

class Tag(models.Model):
    name = models.CharField(max_length=250)