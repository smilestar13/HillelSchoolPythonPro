from django.urls import path
from products.views import ProductsView

from django.conf import settings


urlpatterns = [
    path('', ProductsView.as_view(), name='products')
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # noqa