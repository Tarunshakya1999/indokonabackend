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


urlpatterns = [
    path('', include(router.urls)),
]
