from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from testApi import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('testApi.urls')),
    path('chaining/', include('smart_selects.urls')),
  
    path('api/delete_bank_card/<int:pk>/', views.delete_bank_card, name='delete-bank-card'),
    path('api/update_bank_card/', views.update_status_bank_card, name='update-bank-card'),
    
    path('api/delete_cart_product/<int:pk>/', views.delete_cart_product, name='delete-cart-product'),
    path('api/delete_cart_product_from_prod_id/<int:pk>/', views.delete_cart_product_from_prod_id, name='delete-cart-product'),
    path('api/add_cart_product/', views.add_product_to_cart, name='add-cart-product'),
    path('api/add_to_on_road/', views.add_product_to_onroad, name='add-to-on-road'),
    
    path('api/cat_with_sub/', views.get_categories_with_subcategories, name='cat-with-sub'),
    path('api/add_product/', views.add_product, name='add-product'),
    path('api/status_delivery_point/<int:id>/', views.status_delivery_point, name='status-delivery-point'),
    path('api/choice_delivery_point/<int:id>/', views.choice_delivery_point, name='choice-delivery-point'),
    
    path('api/get_sizes_and_colors/<int:id>/', views.get_sizes_and_colors, name='get-sizes-and-colors'),
    path('api/get_particular_sizes/<path:params>/', views.get_sizes, name='get-particular-sizes'),
    
    path('api/add_delivery_point_comment/', views.add_delivery_point_comment, name='add-delivery-point-comment'),

    path('api/register/', views.RegistrationAPIView.as_view(), name='register'),
    path('api/login/', views.LoginAPIView.as_view(), name='login'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('api/test/', views.ProfileView.as_view(), name='testtt'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)