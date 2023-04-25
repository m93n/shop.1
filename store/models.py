from django.db import models
from django.urls import reverse
from datetime import datetime, timedelta
import pytz

datetime_now = datetime.now(tz=pytz.utc)

RATE_CHOICES = [
    ("0.5",0.5),
    ("1",1),
    ("1.5",1.5),
    ("2",2),
    ("2.5",2.5),
    ("3",3),
    ("3.5",3.5),
    ("4",4),
    ("4.5",4.5),
    ("5",5),
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
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    sku = models.IntegerField(blank=True)
    available = models.BooleanField(default=True)
    tag = models.ManyToManyField('Tag')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def check_new_product(self):

        new_product_datetime_length = datetime_now - timedelta(weeks=2)
        if self.created >= new_product_datetime_length:
            return True
        
        return False

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

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['date_added',]

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.product.sale_price * self.quantity
    
    def __str__(self):
        return self.product

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
    rate = models.CharField(max_length=4, choices=RATE_CHOICES)
    created = models.DateTimeField()

    def __str__(self):
        return self.product.name

class Tag(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    