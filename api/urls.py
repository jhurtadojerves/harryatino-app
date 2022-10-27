"""URLs api rest"""

# Local
# Urls
from api.products import router as products_router
from api.purchases import router as purchases_router

urlpatterns = []
urlpatterns.extend(products_router.urlpatterns)
urlpatterns.extend(purchases_router.urlpatterns)
