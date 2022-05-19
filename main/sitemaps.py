from django.contrib import sitemaps
from django.shortcuts import reverse
# from products.models import Product,Category

class StaticViewSitemap(sitemaps.Sitemap):
    def items(self):
        return ['home','select_class']
    def location(self , item):
        return reverse(item) 
        
