from . import views
from rest_framework import routers

app_name = 'api'
router = routers.DefaultRouter()
router.register('cars', views.CarViewSet, 'cars')
urlpatterns = router.urls
