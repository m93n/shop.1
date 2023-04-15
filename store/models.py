from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

RATE_CHOICES = [
    ("1",0.5),
    ("2",1),
    ("3",1.5),
    ("4",2),
    ("5",2.5),
    ("6",3),
    ("7",3.5),
    ("8",4),
    ("9",4.5),
    ("10",5),
]

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

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

    def get_first_image(self):

        images = self.image_set.all()

        product = Product.objects.get(id=self.id)

        # check for exist of image object or create a new
        if not images:
            image = self.image_set.create(name=self.name, image='product/product-grey-7.jpg', product=product)
            image.save()
            image_url = image.image.url
        
        else:
            fisrt_image = images[0]
            image_url = fisrt_image.image.url

        return image_url

    def __str__(self):
        return self.name

class Image(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    email = models.EmailField()
    review = models.TextField()
    rate = models.CharField(max_length=2, choices=RATE_CHOICES)
    created = models.DateTimeField()

    def __str__(self):
        return self.product.name

class Tag(models.Model):
    name = models.CharField(max_length=250)