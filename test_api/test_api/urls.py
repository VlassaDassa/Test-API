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
    path('api/add_cart_product/<int:pk>/', views.add_product_to_cart, name='add-cart-product'),
    path('api/add_to_on_road/', views.add_product_to_onroad, name='add-to-on-road'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)