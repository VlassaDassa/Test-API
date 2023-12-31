from rest_framework import viewsets, status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import models
from . import serializers
import time




# Receiving all categories
class CategoryViewsSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    

# Adding bank card
class AddBankCardViewSet(viewsets.ViewSet):
    queryset = models.BankCards.objects.all()
    serializer_class = serializers.BankCardsSerializer
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
# Deleting bank card
@api_view(['DELETE'])
def delete_bank_card(request, pk):
    try:
        record = models.BankCards.objects.get(pk=pk)
        record.delete()
        return Response(status=status.HTTP_200_OK)
    except models.BankCards.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
# Updating statis bank card
@api_view(['PUT'])
def update_status_bank_card(request):
    try:
        card_id = request.data.get('id')
        new_value = request.data.get('newValue') 

        card = models.BankCards.objects.get(pk=card_id)

        card.main_card = new_value
        card.save()
        
        models.BankCards.objects.exclude(pk=card_id).update(main_card=False)

        return Response(status=status.HTTP_200_OK)
    except models.BankCards.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    
# Receiving all bank cards
class BankCardsViewsSet(viewsets.ModelViewSet):
    queryset = models.BankCards.objects.all()
    serializer_class = serializers.BankCardsSerializer
    
    
# Receiving all delivery points
class DeliveryPointViewsSet(viewsets.ModelViewSet):
    queryset = models.DeliveryPoints.objects.all()
    serializer_class = serializers.DeliveryPointSerializer
    
    
# Receiving all products
class AllProductViewsSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    

# Receiving few products
class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    
    def get_queryset(self):
        start_index = int(self.kwargs['start_limit'])
        count = int(self.kwargs['count'])
        products = self.queryset[start_index:count]
        return products
        
    def list(self, request, *args, **kwargs):
        products = self.get_queryset()
        serializer = self.get_serializer(products, many=True)
        count_products = len(self.queryset)
        
        response_data = {
            'count_products': count_products,
            'products': serializer.data,
        }
        
        return Response(response_data)
   
    

# Receiving particular subcategory
class SubCategoryViewsSet(viewsets.ModelViewSet):
    serializer_class = serializers.SubcategorySerializer
    queryset = models.Subcategory.objects.all()
    
    def get_queryset(self):
        category_id = self.kwargs['id']
        return models.Subcategory.objects.filter(category__id = category_id)

    
# Receiving all slider photos
class SliderPhotoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.SliderPhoto.objects.all()
    serializer_class = serializers.SliderPhotoSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        unwanted_fields = {'big_photo_url', 'medium_photo_url', 'small_photo_url'}
        for item in response.data:
            for field in unwanted_fields:
                item.pop(field, None)
        return response
    
    
class DeliverySliderViewsSet(viewsets.ModelViewSet):
    queryset = models.DeliverySlider.objects.all()
    serializer_class = serializers.DeliverySliderSerializer
    
    
# Receiving all cart products
class CartProductViewsSet(viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartProductSerializer
    

# Deleting cart product
@api_view(['DELETE'])
def delete_cart_product(request, pk):
    try:
        record = models.Cart.objects.get(pk=pk)
        record.delete()
        return Response(status=status.HTTP_200_OK)
    except models.Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
# Deleting cart product from product_id
@api_view(['DELETE'])
def delete_cart_product_from_prod_id(request, pk):
    try:
        models.Cart.objects.filter(product_id=pk).delete()
        return Response(status=status.HTTP_200_OK)
    except models.Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

# Adding cart product
@api_view(['POST'])
def add_product_to_cart(request, pk):
    if request.method == 'POST':
        product_id = pk

        try:
            product = models.Product.objects.get(pk=product_id)
        except models.Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = models.Cart.objects.get_or_create(product=product)
        serializer = serializers.CartProductSerializer(cart_item)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
# Getting current delivery point
class CurrentDeliveryPointViewsSet(viewsets.ModelViewSet):
    serializer_class = serializers.DeliveryPointSerializer
    queryset = models.DeliveryPoints.objects.filter(seleceted=True)
    
    
# Getting current bank card
class CurrentBankCardViewsSet(viewsets.ModelViewSet):
    serializer_class = serializers.BankCardsSerializer
    queryset = models.BankCards.objects.filter(main_card=True)
    

# Adding product to "OnRoad" model
@api_view(['POST'])
def add_product_to_onroad(request):
    if request.method == 'POST':
        try:
            data = request.data
            product_items = data.get('products', [])
            bank_card_id = data.get('bank_card_id')
            delivery_point_id = data.get('delivery_point_id')

            bank_card = models.BankCards.objects.get(pk=bank_card_id)
            delivery_point = models.DeliveryPoints.objects.get(pk=delivery_point_id)

            total_price = 0

            onroad_items = []

            cart_ids_to_delete = []

            with transaction.atomic():
                for product_item in product_items:
                    cart_id = product_item.get('product_id')
                    total_price_item = product_item.get('total_price')

                    cart = models.Cart.objects.get(pk=cart_id)

                    product = cart.product

                    total_price += total_price_item

                    onroad_item = models.OnRoad(
                        product=product,
                        bank_card=bank_card,
                        delivery_point=delivery_point,
                        totalPrice=total_price_item
                    )
                    onroad_items.append(onroad_item)

                    cart_ids_to_delete.append(cart_id)

                models.OnRoad.objects.bulk_create(onroad_items)

                models.Cart.objects.filter(pk__in=cart_ids_to_delete).delete()

            return Response({'message': 'Products added to OnRoad and removed from Cart'}, status=status.HTTP_200_OK)
        except models.Cart.DoesNotExist:
            return Response({'error': 'One or more Cart items not found'}, status=status.HTTP_404_NOT_FOUND)

        