from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(max_length=200, blank=True)
    category_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = "Categories"

    def get_url(self):
        return reverse('store:product_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
