from typing import Iterable, Optional
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import pytz
import PIL.Image

# change email field of default User model to unique=True
User._meta.get_field('email')._unique = True

datetime_now = datetime.now(tz=pytz.utc)

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
    tags = models.ManyToManyField('Tag')
    avarage_rate = models.DecimalField(max_digits=2, decimal_places=1)
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
        return self.product.name
    
class Order(models.Model):
    token = models.CharField(max_length=250, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Order Total')
    emailAddress = models.EmailField(max_length=250, blank=True, verbose_name='Email Address')
    created = models.DateTimeField(auto_now_add=True)
    billingName = models.CharField(max_length=250, blank=True)
    billingAddress1 = models.CharField(max_length=250, blank=True)
    billingCity = models.CharField(max_length=250, blank=True)
    billingPostcode = models.CharField(max_length=250, blank=True)
    billingCountry = models.CharField(max_length=250, blank=True)
    shippingName = models.CharField(max_length=250, blank=True)
    shippingAddress1 = models.CharField(max_length=250, blank=True)
    shippingCity = models.CharField(max_length=250, blank=True)
    shippingPostcode = models.CharField(max_length=250, blank=True)
    shippingCountry = models.CharField(max_length=250, blank=True)

    class Meta:
        db_table = 'Order'
        ordering = ['-created']

    def __str__(self):
        return str(self.id)
    
class OrderItem(models.Model):
    product = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Price')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'OrderItem'

    def sub_total(self):
        return self.quantity * self.price

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
    rate = models.DecimalField(max_digits=2, decimal_places=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

class Tag(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(
        default='avatar.jpg', 
        upload_to='profile'
    )

    def __str__(self):
        
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
        with PIL.Image.open(self.avatar.path) as img:
            if img.height > 400 or img.width > 400:
                output_size = (400, 400)

                img.thumbnail(output_size)
                
                img.save(self.avatar.path) 
    