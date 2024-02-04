from rest_framework import routers
from testApi import views

router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewsSet)
router.register(r'subcategory/(?P<id>\d+)', views.SubCategoryViewsSet)
router.register(r'slider', views.SliderPhotoViewSet)
router.register(r'all_products', views.AllProductViewsSet)

router.register(r'all_delivery_points', views.DeliveryPointViewsSet)

router.register(r'get_user_bank_cards/(?P<user_id>\d+)', views.BankCardsViewsSet)
router.register(r'add_bank_card/(?P<user_id>\d+)', views.AddBankCardViewSet, basename='bankcards')

router.register(r'^products/(?P<start_limit>\d+)/(?P<count>\d+)', views.ProductViewSet)
router.register(r'^deliveryslider', views.DeliverySliderViewsSet)

router.register(r'cart_products/(?P<user_id>\d+)', views.CartProductViewsSet)
router.register(r'get_current_card/(?P<user_id>\d+)', views.CurrentBankCardViewsSet, basename='bankcards')

router.register(r'get_characteristics_fields/(?P<id>\d+)', views.CharacteristicsFieldsViewsSet)
router.register(r'get_colors', views.ColorViewsSet)
router.register(r'get_sizes', views.SizeViewsSet)

router.register(r'get_delivery_point/(?P<id>\d+)', views.ParticularDeliveryPoint)






urlpatterns = router.urls

