from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from testApi import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('testApi.urls')),
    path('api/delete_bank_card/<int:pk>/', views.delete_bank_card, name='delete-bank-card'),
    path('api/update_bank_card/', views.update_status_bank_card, name='update-bank-card'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)