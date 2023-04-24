from django.urls import path
from products.views import ProductsView, ExportToPdf, ExportToCSV, ImportCSV

from django.conf import settings


urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('export-csv/', ExportToCSV.as_view(), name='products_to_csv'),
    path('export-pdf/', ExportToPdf.as_view(), name='products_to_pdf'),
    path('import-csv/', ImportCSV.as_view(), name='products_from_csv'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # noqa