from django.db import models
from smart_selects.db_fields import ChainedForeignKey



class Category(models.Model):
    icon = models.FileField(upload_to='images/category_icon')
    category_name = models.CharField(max_length=100, unique=True, blank=False)

    def __str__(self):
        return self.category_name


class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=100, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.subcategory_name
    
    
class SliderPhoto(models.Model):
    big_photo = models.ImageField(upload_to='images/slider')
    medium_photo = models.ImageField(upload_to='images/slider')
    small_photo = models.ImageField(upload_to='images/slider')
    
    
class Product(models.Model):
    name = models.CharField(max_length=100, blank=False)
    product_photo = models.ImageField(upload_to='images/product_photo')
    price = models.IntegerField(blank=False)
    rating = models.IntegerField(blank=False)
    count_feedbacks = models.IntegerField(blank=False)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='subcategory')
    
    def __str__(self):
        return self.name
    

class ColorModel(models.Model):
    color = models.CharField(max_length=50, null=False, blank=False)
    color_value = models.CharField(max_length=50, null=False, blank=False)
    
    def __str__(self):
        return str(self.color)
    

class SizeModel(models.Model):
    size = models.CharField(max_length=50, null=False, blank=False)
    size_value = models.CharField(max_length=50, null=False, blank=False)
    
    def __str__(self):
        return str(self.size)
    
    
class ProductCharacteristics(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = ChainedForeignKey(
        Subcategory,
        chained_field="category",
        chained_model_field="category", 
    )
    
    color = models.BooleanField(default=False)
    size = models.BooleanField(default=False)
    fields = models.JSONField()
    
    def __str__(self):
        return str(self.subcategory.subcategory_name)
    
    
class DeliveryPoints(models.Model):
    photo = models.ImageField(upload_to='images/delivery_point')
    city = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=50, blank=False)
    schedule = models.CharField(max_length=50, blank=False)
    rating = models.IntegerField(blank=False)
    coord_x = models.FloatField(blank=False)
    coord_y = models.FloatField(blank=False)
    seleceted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.address
    
   
class BankCards(models.Model):
    card_number = models.IntegerField(blank=False)
    month = models.IntegerField(blank=False)
    year = models.IntegerField(blank=False)
    main_card = models.BooleanField(blank=False, default=False)
    bank_ico = models.FileField(upload_to='images/bankIcons', default="images/bankIcons/question.svg")
    
    def __str__(self):
        return str(self.card_number)
    

class DeliverySlider(models.Model):
    photo = models.ImageField(upload_to='images/deliveryslider')


    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default = 0)
    isChecked = models.BooleanField(default = False)
    totalCount = models.IntegerField(default = 15)

    def __str__(self):
        return str(self.product.name)
    
    
class OnRoad(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bank_card = models.ForeignKey(BankCards, on_delete=models.CASCADE)
    delivery_point = models.ForeignKey(DeliveryPoints, on_delete=models.CASCADE)
    totalPrice = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.product.name)
    




