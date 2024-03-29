from rest_framework import serializers
from django.core.exceptions import ValidationError
from . import models



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'
        

class BankCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BankCards
        fields = '__all__'

        
        
class DeliveryPointCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeliveryPointComments
        fields = '__all__'
        
        

class DeliveryPointPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeliveryPointPhoto
        fields = '__all__'
        


class DeliveryPointSerializer(serializers.ModelSerializer):
    photos = DeliveryPointPhotoSerializer(many=True, read_only=True)
    comments = DeliveryPointCommentsSerializer(many=True, read_only=True, source='deliverypointcomments_set')
    
    class Meta:
        model = models.DeliveryPoints
        fields = '__all__'
        
        
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subcategory
        fields = '__all__'
        

class ProductCharacteristicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCharacteristics
        fields = '__all__'
        
        
class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductPhoto
        fields = '__all__'
        
        
class ProductSerializer(serializers.ModelSerializer):
    subcategory_name = serializers.CharField(source='subcategory.subcategory_name', read_only=True)
    is_in_cart = serializers.SerializerMethodField()
    product_photo = ProductPhotoSerializer(many=True) 
    main_photo = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = ['id', 'subcategory', 'count', 'subcategory_name', 'name', 'product_photo', 'characteristics', 'main_photo', 'price', 'rating', 'count_feedbacks', 'is_in_cart']

    def get_main_photo(self, obj):
        request = self.context.get('request')
        if obj.main_photo:
            return request.build_absolute_uri(obj.main_photo.url)
        return None

    def get_is_in_cart(self, obj):
        cart_exists = models.Cart.objects.filter(product=obj).exists()
        return cart_exists
        
        
class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'

        
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
    product_id = serializers.IntegerField(source="product.id")
    subcategory = serializers.CharField(source='product.subcategory.subcategory_name')
    name = serializers.CharField(source='product.name')
    price = serializers.IntegerField(source='product.price')
    rating = serializers.IntegerField(source='product.rating')
    count_feedbacks = serializers.IntegerField(source='product.count_feedbacks')
    main_photo = serializers.ImageField(source='product.main_photo')
    size_value = serializers.CharField(source='size.size', allow_null=True, required=False)
    color_value = serializers.CharField(source='color.color_value', allow_null=True, required=False)
    

    class Meta:
        model = models.Cart
        fields = ['id', 'product_id', 'color_value', 'size_value', 'size', 'count', 'totalCount', 'isChecked', 'subcategory', 'name', 'main_photo', 'price', 'rating', 'count_feedbacks']
        
        
class OnRoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OnRoad
        fields = '__all__'
        
    
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ColorModel
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SizeModel
        fields = '__all__'
        


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['id', 'username', 'phone_number', 'is_seller', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            user = models.CustomUser.objects.create_user(**validated_data)
            return user
        except ValidationError as e:
            raise serializers.ValidationError({'error': str(e)})



class UserPurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserPurchases
        fields = '__all__' 