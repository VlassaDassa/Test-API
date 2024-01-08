from django.http import JsonResponse
from django.db.models import F
from rest_framework import viewsets, status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import models
from . import serializers
import json
from django.db.models import F
from django.shortcuts import get_object_or_404




# Receiving all categories
class CategoryViewsSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    
    
# Get categories and relate subcategories
def get_categories_with_subcategories(request):
    categories = models.Category.objects.prefetch_related('subcategories').all()
    result_data = []

    for category in categories:
        category_data = serializers.CategorySerializer(category).data

        formatted_subcategories = []

        for subcategory in category.subcategories.all():
            subcategory_data = serializers.SubcategorySerializer(subcategory).data
            formatted_subcategories.append({
                'subcategory_id': subcategory_data['id'],
                'subcategory_name': subcategory_data['subcategory_name']
            })

        result_data.append({
            'category_id': category_data['id'],
            'category_name': category_data['category_name'],
            'subcategory': formatted_subcategories
        })

    return JsonResponse(result_data, safe=False)
    

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
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    lookup_field = 'id'
    
    def get_queryset(self):
        start_index = int(self.kwargs['start_limit'])
        count = int(self.kwargs['count'])
        products = models.Product.objects.annotate(row_number=F('id')).order_by('id')[start_index:count]

        return products
        
    def list(self, request, *args, **kwargs):
        products = self.get_queryset()
        serializer = self.get_serializer(products, many=True)
        count_products = models.Product.objects.count()
        
        response_data = {
            'count_products': count_products,
            'products': serializer.data,
        }
        
        return Response(response_data)
        
    def list(self, request, *args, **kwargs):
        products = self.get_queryset()
        serializer = self.get_serializer(products, many=True)
        count_products = models.Product.objects.count()
        
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

    
# Receiving all slider photos for index
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
    
    
# Get photos for delivery slider
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
    


@api_view(['POST'])
def add_product_to_cart(request):
    
    product_id = request.data.get('product_id')
    count = request.data.get('count')
    get_color = request.data.get('color', {}).get('selectColor')
    get_size = request.data.get('size', {}).get('selectSize')
    relateInputs = request.data.get('relateInputs')
        
    try:
        if get_color:
            color = get_object_or_404(models.ColorModel, color_value=get_color)
        else:
            color = get_color
            
        if get_size:
            size = get_object_or_404(models.SizeModel, size_value=get_size)
        else:
            size = get_size
            
        if relateInputs:
            color = get_object_or_404(models.ColorModel, color_value=relateInputs.get('color'))
            size = get_object_or_404(models.SizeModel, size_value=relateInputs.get('size'))
            
        
        product = get_object_or_404(models.Product, id=int(product_id))
        models.Cart.objects.create(product=product, count=int(count), color=color, size=size)
    except Exception as ex:
        print(ex)
        return Response({'error': 'error'}, status=status.HTTP_404_NOT_FOUND)
        
    return Response({'message': 'Success!'}, status=200)
    
    
    
    
# Getting current delivery point
class CurrentDeliveryPointViewsSet(viewsets.ModelViewSet):
    serializer_class = serializers.MyDeliveryPointSerializer
    queryset = models.MyDeliveryPoint.objects.all()
    
    
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
            product_items = data.get('prod_data', [])
            bank_card_id = data.get('bank_card_id')
            delivery_point_id = data.get('delivery_point_id')
            
            onroad_items = []
            cart_ids_to_delete = []
            
            bank_card = models.BankCards.objects.get(pk=bank_card_id)
            delivery_point = models.MyDeliveryPoint.objects.get(pk=delivery_point_id).delivery_point
            

            with transaction.atomic():
                for product_item in product_items:
                    cart_id = product_item.get('item_id')
                    total_price_item = product_item.get('total_price')
                    total_count_item = product_item.get('total_count')
                    color_val = product_item.get('color')
                    size_id = product_item.get('size')

                    cart = models.Cart.objects.get(pk=cart_id)
                    
                    color = models.ColorModel.objects.get(color_value=color_val) if color_val else None
                    size = models.SizeModel.objects.get(pk=size_id) if size_id else None
                    
                    product = cart.product

                    onroad_item = models.OnRoad(
                        product=product,
                        bank_card=bank_card,
                        delivery_point=delivery_point,
                        totalPrice=total_price_item,
                        totalCount=total_count_item,
                        color=color,
                        size=size
                    )
                    onroad_items.append(onroad_item)

                    cart_ids_to_delete.append(cart_id)
                    
                    
                    # Уменьшение количества, обновление состояния "В наличии" в модели Products, в зависимости от категории
                    if color and size:
                        for key, value in list(product.characteristics.items()):
                            if key.startswith("relateInput"):
                                if isinstance(value, dict) and value.get("color") == color_val and value.get("size") == size.size_value:
                                    count = int(value.get("count", 0))
                                    count -= int(total_count_item)
                                    if count <= 0:
                                        count = 0
                                        product.characteristics.pop(key, None)
                                    else:
                                        value["count"] = str(count)
                        
                        # Определение наличия товара, если хотя бы 1 count в relateInput != 0             
                        relate_inputs_count_zero = all(
                            int(value["count"]) <= 0
                            for key, value in product.characteristics.items()
                            if key.startswith("relateInput")
                        )

                        for key, value in list(product.characteristics.items()):
                            if key.startswith("relateInput"):
                                count = int(value.get("count", 0))
                                if count > 0:
                                    relate_inputs_count_zero = False
                                    break

                        if relate_inputs_count_zero:
                            product.characteristics['in_stock'] = False

                        models.Product.objects.filter(pk=product.pk).update(characteristics=product.characteristics)
                                    

                    
                    elif color and not size:
                        flag = False
                        for item in product.characteristics.get('color', []):
                            if item.get('selectColor') == color_val:
                                count = int(item.get('countColor', 0)) - int(total_count_item)

                                if count <= 0:
                                    product.characteristics['color'] = [i for i in product.characteristics['color'] if i['selectColor'] != color_val]
                                    models.Product.objects.filter(pk=product.pk).update(characteristics=product.characteristics)
                                else:
                                    item['countColor'] = count
                                
                        # Определение наличия товара, если хотя бы 1 count в relateInput != 0  
                        for i in product.characteristics.get('color', []):
                            if int(i['countColor']) > 0:
                                flag = True
                                
                        product.characteristics['in_stock'] = flag
                        models.Product.objects.filter(pk=product.pk).update(characteristics=product.characteristics)
                                
                            
                        
                    elif size and not color:
                        flag = False
                        for item in product.characteristics.get('size', []):
                            if item.get('selectSize') == size.size_value:
                                count = int(item.get('countSize', 0)) - int(total_count_item)

                                if count <= 0:
                                    product.characteristics['size'] = [i for i in product.characteristics['size'] if i['selectSize'] != size.size_value]
                                    models.Product.objects.filter(pk=product.pk).update(characteristics=product.characteristics)
                                else:
                                    item['countSize'] = count
                    
                        # Определение наличия товара, если хотя бы 1 count в relateInput != 0  
                        for i in product.characteristics.get('size', []):
                            if int(i['countSize']) > 0:
                                flag = True
                                    
                        product.characteristics['in_stock'] = flag
                        models.Product.objects.filter(pk=product.pk).update(characteristics=product.characteristics)
                                
                            
                    else:
                        count = product.count = int(product.count) - int(total_count_item) 
                        if count <= 0:
                           product.characteristics['in_stock'] = False
                        
                        models.Product.objects.filter(pk=product.pk).update(characteristics=F('characteristics'))
                        product.save()
                    
                    
                
                models.OnRoad.objects.bulk_create(onroad_items)
                models.Cart.objects.filter(pk__in=cart_ids_to_delete).delete()
                
            return Response({'message': 'Products added to OnRoad and removed from Cart'}, status=status.HTTP_200_OK)
        except models.Cart.DoesNotExist:
            return Response({'error': 'One or more Cart items not found'}, status=status.HTTP_404_NOT_FOUND)

        
# Receiving characteristics fields
class CharacteristicsFieldsViewsSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductCharacteristicsSerializer
    queryset = models.ProductCharacteristics.objects.all()
    
    def get_queryset(self):
        subcategory__id = self.kwargs['id']
        return models.ProductCharacteristics.objects.filter(subcategory__id=subcategory__id)


# Receiving all colors
class ColorViewsSet(viewsets.ModelViewSet):
    queryset = models.ColorModel.objects.all()
    serializer_class = serializers.ColorSerializer
    
    
# Receiving all sizes
class SizeViewsSet(viewsets.ModelViewSet):
    queryset = models.SizeModel.objects.all()
    serializer_class = serializers.SizeSerializer
    

@api_view(['POST'])
def add_product(request):
    name = request.data.get('name')
    price = int(request.data.get('price'))
    count = int(request.data.get('count'))
    subcategory = int(request.data.get('subcategory'))
    characteristics = request.data.get('characteristics')
    description = request.data.get('description')
    
    
    # Creating object of Product
    product = models.Product.objects.create(
        name=name,
        price=price,
        count=count,
        subcategory_id=subcategory,
        characteristics=json.loads(characteristics),
        description=description,
        main_photo=request.FILES['mainPhoto'],
    )

    # Handling photos and creating objects ProductPhoto
    product_photos = request.FILES.getlist('product_photo')
    for photo in product_photos:
        product_photo = models.ProductPhoto.objects.create(photo=photo)
        product.product_photo.add(product_photo)
    

    return Response({'message': 'Success!'}, status=200)


# Receiving all data for particular delivery point
class ParticularDeliveryPoint(viewsets.ModelViewSet):
    queryset = models.DeliveryPoints.objects.all()
    serializer_class = serializers.DeliveryPointSerializer
    
    def get_queryset(self):
        delivery_point_id = self.kwargs['id']
        delivery_point_data = self.queryset.filter(id=delivery_point_id)
        
        return delivery_point_data
    
    
# Receiving status delivery point
@api_view(['GET'])
def status_delivery_point(request, id):
    delivery_point_status = models.MyDeliveryPoint.objects.filter(delivery_point__id=id).exists()

    if delivery_point_status:
        return Response({'exists': True}, status=200)
    else:
        return Response({'exists': False}, status=200)
    

# Choice delivery point
@api_view(['PUT'])
def choice_delivery_point(request, id):
    try:
        # Clear old
        models.MyDeliveryPoint.objects.all().delete()
        models.MyDeliveryPoint.objects.create(delivery_point_id=id)
        
        return Response({'Message': 'Success!'}, status=200)
        
    except Exception as e:
        return Response({'Error': e}, status=404)
    
    
# Getting sizes, colors or relate inputs for product
@api_view(['GET'])
def get_sizes_and_colors(request, id):
    product = models.Product.objects.get(id=id)
    
    exists_relate_inputs = [key for key in product.characteristics if key.startswith('relateInput')]
    
    send_data = {
        'exists': False,
        'exists_relateInputs': False,
        'exists_colors': False,
        'exists_sizes': False,
        'relateInputs': [],
        'colors': [],
        'sizes': [],
    }
    
    if (exists_relate_inputs):
        send_data['exists'] = True
        send_data['exists_relateInputs'] = True
        send_data['relateInputs'] = [product.characteristics[key] for key in exists_relate_inputs]
        
    elif (product.characteristics.get('size')):
        send_data['exists'] = True
        send_data['exists_sizes'] = True
        send_data['sizes'] = product.characteristics['size']
        
    elif (product.characteristics.get('color')):
        send_data['exists'] = True
        send_data['exists_colors'] = True
        send_data['colors'] = product.characteristics['color']
        
    else:
        send_data['count'] = product.count
    
    
    return JsonResponse(send_data)
    
    

# Get sizes
@api_view(['GET'])
def get_sizes(request, params):
    sizes = models.SizeModel.objects.filter(id__in=params.split('/'))
    
    if sizes:
        serialized_sizes = [{"display_name": size.size, "value": size.size_value} for size in sizes]
        return JsonResponse(serialized_sizes, safe=False)
    else:
        return Response({'Error': 'not found'}, status=404)
    
    

# Add delivery point comment
@api_view(['POST'])
def add_delivery_point_comment(request):
    username = request.data.get('username')
    rating = request.data.get('rating')
    content = request.data.get('content')
    delivery_point_id = request.data.get('deliveryPointId')
    
    try:    
        # Creating comment
        delivery_point = get_object_or_404(models.DeliveryPoints, id=int(delivery_point_id))
        
        models.DeliveryPointComments.objects.create(
            delivery_point = delivery_point,
            username = username,
            rating = rating,
            content = content
        )
        
        # Calculating rating
        all_comments = models.DeliveryPointComments.objects.filter(delivery_point=delivery_point)
        new_rating = 0
        for i in all_comments:
            new_rating += i.rating
            
        delivery_point.rating = new_rating/len(all_comments)
        delivery_point.save()
            
        
        
    except Exception as ex:
        print(ex)
        return Response({'Error': 'error'}, status=404)
    
    
    return Response({'Success': 'success!'}, status=200)

    

    

    
    
   
            