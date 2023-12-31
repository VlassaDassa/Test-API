from rest_framework import serializers
from . import models



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'
        

class BankCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BankCards
        fields = '__all__'
        
        
class DeliveryPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeliveryPoints
        fields = '__all__'
        
        
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subcategory
        fields = '__all__'
        
        
class ProductSerializer(serializers.ModelSerializer):
    subcategory_name = serializers.CharField(source='subcategory.subcategory_name', read_only=True)
    is_in_cart = serializers.SerializerMethodField()  

    class Meta:
        model = models.Product
        fields = ['id', 'subcategory', 'subcategory_name', 'name', 'product_photo', 'price', 'rating', 'count_feedbacks', 'is_in_cart']  # Включаем is_in_cart в список полей

    def get_is_in_cart(self, obj):
        cart_exists = models.Cart.objects.filter(product=obj).exists()
        return cart_exists
        

        
class SliderPhotoSerializer(serializers.ModelSerializer):
    big_photo_url = serializers.SerializerMethodField()
    medium_photo_url = serializers.SerializerMethodField()
    small_photo_url = serializers.SerializerMethodField()

    def get_big_photo_url(self, obj):
        if obj.big_photo:
            return self.context['request'].build_absolute_uri(obj.big_photo.url)
        return None

    def get_medium_photo_url(self, obj):
        if obj.medium_photo:
            return self.context['request'].build_absolute_uri(obj.medium_photo.url)
        return None

    def get_small_photo_url(self, obj):
        if obj.small_photo:
            return self.context['request'].build_absolute_uri(obj.small_photo.url)
        return None

    class Meta:
        model = models.SliderPhoto
        fields = ['big_photo', 'medium_photo', 'small_photo', 'big_photo_url', 'medium_photo_url', 'small_photo_url']


class DeliverySliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeliverySlider
        fields = '__all__'
        
        
class CartProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.CharField(source='product.subcategory.subcategory_name')
    name = serializers.CharField(source='product.name')
    product_photo = serializers.ImageField(source='product.product_photo')
    price = serializers.IntegerField(source='product.price')
    rating = serializers.IntegerField(source='product.rating')
    count_feedbacks = serializers.IntegerField(source='product.count_feedbacks')

    class Meta:
        model = models.Cart
        fields = ['id', 'count', 'totalCount', 'isChecked', 'subcategory', 'name', 'product_photo', 'price', 'rating', 'count_feedbacks']
        
        
class OnRoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OnRoad
        fields = '__all__'
        
    
