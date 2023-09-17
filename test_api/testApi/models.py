from django.db import models



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
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='subcategory')
    name = models.CharField(max_length=100, blank=False)
    product_photo = models.ImageField(upload_to='images/product_photo')
    price = models.IntegerField(blank=False)
    rating = models.IntegerField(blank=False)
    count_feedbacks = models.IntegerField(blank=False)
    
    def __str__(self):
        return self.name
    
    
class DeliveryPoints(models.Model):
    photo = models.ImageField(upload_to='images/delivery_point')
    city = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=50, blank=False)
    schedule = models.CharField(max_length=50, blank=False)
    rating = models.IntegerField(blank=False)
    coord_x = models.FloatField(blank=False)
    coord_y = models.FloatField(blank=False)
    
    def __str__(self):
        return self.address
    
    
    
class AndreyDelivey(models.Model):
    photo = models.ImageField(upload_to='images/andreyphoto')
   
   
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
    


