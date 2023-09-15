from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Category, Subcategory, SliderPhoto, Product, DeliveryPoints, AndreyDelivey, BankCards
from .serializers import CategorySerializer, SubcategorySerializer, SliderPhotoSerializer, ProductSerializer, DeliveryPointSerializer, AndreySerializer, BankCardsSerializer
import time





class CategoryViewsSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
class AddBankCardViewSet(viewsets.ViewSet):
    queryset = BankCards.objects.all()
    serializer_class = BankCardsSerializer
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['DELETE'])
def delete_bank_card(request, pk):
    try:
        record = BankCards.objects.get(pk=pk)
        record.delete()
        return Response(status=status.HTTP_200_OK)
    except BankCards.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['PUT'])
def update_status_bank_card(request):
    try:
        card_id = request.data.get('id')
        new_value = request.data.get('newValue') 

        card = BankCards.objects.get(pk=card_id)

        card.main_card = new_value
        card.save()
        
        BankCards.objects.exclude(pk=card_id).update(main_card=False)

        return Response(status=status.HTTP_200_OK)
    except BankCards.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    
        
class BankCardsViewsSet(viewsets.ModelViewSet):
    queryset = BankCards.objects.all()
    serializer_class = BankCardsSerializer
    
    
class DeliveryPointViewsSet(viewsets.ModelViewSet):
    queryset = DeliveryPoints.objects.all()
    serializer_class = DeliveryPointSerializer
    
    
class AndreyViewsSet(viewsets.ModelViewSet):
    queryset = AndreyDelivey.objects.all()
    serializer_class = AndreySerializer
    
    
class AllProductViewsSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
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
   
    
    
class SubCategoryViewsSet(viewsets.ModelViewSet):
    serializer_class = SubcategorySerializer
    queryset = Subcategory.objects.all()
    
    def get_queryset(self):
        category_id = self.kwargs['id']
        return Subcategory.objects.filter(category__id = category_id)

    
class SliderPhotoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SliderPhoto.objects.all()
    serializer_class = SliderPhotoSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        unwanted_fields = {'big_photo_url', 'medium_photo_url', 'small_photo_url'}
        for item in response.data:
            for field in unwanted_fields:
                item.pop(field, None)
        return response
    

