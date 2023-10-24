from django.contrib import admin
from . import models




# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Subcategory)
admin.site.register(models.SliderPhoto)
admin.site.register(models.Product)
admin.site.register(models.DeliveryPoints)
admin.site.register(models.BankCards)
admin.site.register(models.Cart)
admin.site.register(models.OnRoad)
admin.site.register(models.DeliverySlider)

admin.site.register(models.ColorModel)
admin.site.register(models.SizeModel)
admin.site.register(models.ProductCharacteristics)
admin.site.register(models.ProductPhoto)

admin.site.register(models.DeliveryPointComments)
admin.site.register(models.DeliveryPointPhoto)
admin.site.register(models.MyDeliveryPoint)


