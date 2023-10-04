from rest_framework import routers
from testApi import views

router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewsSet)
router.register(r'subcategory/(?P<id>\d+)', views.SubCategoryViewsSet)
router.register(r'slider', views.SliderPhotoViewSet)
router.register(r'all_products', views.AllProductViewsSet)

router.register(r'all_delivery_points', views.DeliveryPointViewsSet)

router.register(r'all_bank_cards', views.BankCardsViewsSet)
router.register(r'add_bank_card', views.AddBankCardViewSet)

router.register(r'^products/(?P<start_limit>\d+)/(?P<count>\d+)', views.ProductViewSet)

router.register(r'cart_products', views.CartProductViewsSet)
router.register(r'get_current_point', views.CurrentDeliveryPointViewsSet)
router.register(r'get_current_card', views.CurrentBankCardViewsSet)







urlpatterns = router.urls

