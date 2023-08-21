from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Customer)  #this adds the customer database to the admin page
admin.site.register(Product) 
admin.site.register(Tag)
admin.site.register(Order) 
