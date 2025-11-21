from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'hero', HeroViewSet)
router.register(r'pdf', PDFAPI)
router.register(r'plans',PlansAPI)
router.register(r'feedback',TestimonialFeedbackAPI)
router.register(r'myproducts',ProductAPI)
router.register(r'cart', CartAPI)
router.register(r'blogs', BlogViewSet)
router.register(r"useful-links", UsefulLinkViewSet)
# New Urls
# router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'leads', LeadViewSet)
router.register(r'wallets', WalletViewSet)
router.register(r'commissions', CommissionViewSet)
router.register(r'hotdeals', HotDealViewSet)
router.register(r'userprofiles', PublicProfileViewSet)
router.register(r'myreels', MyReelsViewSet)
router.register(r'mypost', MypostViewSet)




urlpatterns = [
    path('', include(router.urls)),
]
