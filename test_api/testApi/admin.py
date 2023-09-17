from django.contrib import admin
from .models import Category, Subcategory, SliderPhoto, Product, DeliveryPoints, AndreyDelivey, BankCards, DeliverySlider

# Register your models here.
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(SliderPhoto)
admin.site.register(Product)
admin.site.register(DeliveryPoints)
admin.site.register(AndreyDelivey)
admin.site.register(BankCards)
admin.site.register(DeliverySlider)

