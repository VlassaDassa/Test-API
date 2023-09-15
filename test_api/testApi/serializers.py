from rest_framework import serializers
from .models import Category, Subcategory, SliderPhoto, Product, DeliveryPoints, AndreyDelivey, BankCards




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        

class BankCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCards
        fields = '__all__'
        
        
class AndreySerializer(serializers.ModelSerializer):
    class Meta:
        model = AndreyDelivey
        fields = '__all__'
        
        
class DeliveryPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPoints
        fields = '__all__'
        
        
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'
        
        
class ProductSerializer(serializers.ModelSerializer):
    subcategory_name = serializers.CharField(source='subcategory.subcategory_name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'subcategory', 'subcategory_name', 'name', 'product_photo', 'price', 'rating', 'count_feedbacks']
        
        
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
        model = SliderPhoto
        fields = ['big_photo', 'medium_photo', 'small_photo', 'big_photo_url', 'medium_photo_url', 'small_photo_url']


