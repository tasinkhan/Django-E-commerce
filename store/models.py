from django.db import models
from django.urls import reverse
from category.models import Category
# Create your models here.
class Product(models.Model):
    category             = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name         = models.CharField(max_length=200, unique=True)
    slug                 = models.SlugField(max_length=200,unique=True)
    description          = models.TextField(max_length=200, blank=True)
    price                = models.IntegerField()
    stock                = models.IntegerField()
    images               = models.ImageField(upload_to='photos/products')
    is_available         = models.BooleanField(default=True)
    created_date         = models.DateTimeField(auto_now_add=True)
    modified_date        = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('store:product_detail', args=[self.category.slug, self.slug])
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.product_name

Variation_category_choice = (
    ('color','color'),
    ('size', 'size'),
)

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=200, choices=Variation_category_choice)
    variation_values = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = VariationManager()

    def __unicode__(self):
        self.product