from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'hero', HeroViewSet)
router.register(r'pdf', PDFAPI)
router.register(r'plans',PlansAPI)
router.register(r'feedback',TestimonialFeedbackAPI)
router.register(r'product',ProductAPI)
router.register(r'cart', CartAPI)
router.register('blogs', BlogViewSet)
# New Urls
router.register('products', ProductViewSet)
router.register('orders', OrderViewSet)
router.register('leads', LeadViewSet)
router.register('wallets', WalletViewSet)
router.register('commissions', CommissionViewSet)
router.register('hotdeals', HotDealViewSet)




urlpatterns = [
    path('', include(router.urls)),
]
