from django.urls import path
from products.views import products

from django.conf import settings


urlpatterns = [
    path('', products)
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # noqa