from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import pytz

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
    avarage_rate = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"category_slug": self.category, "product_slug":self.slug})

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

class Image(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='product', default='product/product-grey-7.jpg')
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

class AdditionalInformation(models.Model):
    name = models.CharField(max_length=150)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_choose = models.BooleanField() # it will say each info must choosen by user or its just static info

    def __str__(self):
        return self.name

class AdditionalInformationValue(models.Model):
    name = models.CharField(max_length=250)
    additional_information = models.ForeignKey(AdditionalInformation, on_delete=models.CASCADE)
    default = models.BooleanField()

    def __str__(self):
        return self.name