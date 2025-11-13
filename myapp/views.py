from rest_framework import viewsets
from .models import *
from .serializers import *
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.serializers import UserRegisterSerializer

class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer


class PDFAPI(viewsets.ModelViewSet):
    queryset = PDF.objects.all()
    serializer_class = PDFSerializer


class PlansAPI(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from rest_framework import viewsets
# from .models import Plan, Testimonial, FAQ
# from .serializers import PlanSerializer, TestimonialSerializer, FAQSerializer

# class PlanViewSet(viewsets.ModelViewSet):
#     queryset = Plan.objects.all()
#     serializer_class = PlanSerializer

# class TestimonialViewSet(viewsets.ModelViewSet):
#     queryset = Testimonial.objects.all()
#     serializer_class = TestimonialSerializer

# class FAQViewSet(viewsets.ModelViewSet):
#     queryset = FAQ.objects.all()
#     serializer_class = FAQSerializer


from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import ContactMessage
from rest_framework.decorators import api_view
# myapp/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactMessageSerializer
from django.core.mail import send_mail

@api_view(['POST'])
def contact_view(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # save to DB

        # Send email
        subject = f"New Contact Message from {serializer.data['name']}"
        body = f"""
        Name: {serializer.data['name']}
        Email: {serializer.data['email']}
        Phone: {serializer.data['phone']}
        Message: {serializer.data['message']}
        """
        send_mail(
            subject,
            body,
            'shakyatarun32@gmail.com',  # sender
            ['shakyatarun32@gmail.com'],  # receiver
            fail_silently=False,
        )

        return Response({"success": "Message sent successfully!"}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views.py
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from .models import Testimonial
from .serializers import TestimonialSerializer

class TestimonialFeedbackAPI(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    parser_classes = (MultiPartParser, FormParser)  # <-- ye add karo



from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from .models import DigitalProducts, Cart
from .serializers import ProductSerializer, CartSerializer
from rest_framework.permissions import AllowAny

class ProductAPI(viewsets.ModelViewSet):
    queryset = DigitalProducts.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser)
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]
    
class CartAPI(viewsets.ModelViewSet):
    queryset = Cart.objects.all()  # ✅ Add this
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-id')
    serializer_class = BlogSerializer




# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from django.shortcuts import get_object_or_404
# from .models import DigitalProducts

# @api_view(['GET'])
# def product_share_api(request, id):
#     product = get_object_or_404(DigitalProducts, id=id)

#     data = {
#         "id": product.id,
#         "title": product.productname,
#         "description": product.productdescription,
#         "image": request.build_absolute_uri(product.productimg.url) if product.productimg else "",
#         "share_url": f"https://indokona.com/share/product/{id}/",
#         "product_url": f"https://indokona.com/product/{id}"
#     }

#     return Response(data)







# New Views.py 



from rest_framework import viewsets, permissions
from .models import Product, Order, Lead, Wallet, Commission, HotDeal
from .serializers import ProductSerializer, OrderSerializer, LeadSerializer, WalletSerializer, CommissionSerializer, HotDealSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
   queryset = Product.objects.all().order_by('-created_at')
   serializer_class = ProductSerializer
   permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
   queryset = Order.objects.all().order_by('-created_at')
   serializer_class = OrderSerializer
   permission_classes = [permissions.IsAuthenticated]


class LeadViewSet(viewsets.ModelViewSet):
   queryset = Lead.objects.all().order_by('-created_at')
   serializer_class = LeadSerializer
   permission_classes = [permissions.IsAuthenticated]


class WalletViewSet(viewsets.ModelViewSet):
  queryset = Wallet.objects.all()
  serializer_class = WalletSerializer
  permission_classes = [permissions.IsAuthenticated]


class CommissionViewSet(viewsets.ModelViewSet):
   queryset = Commission.objects.all()
   serializer_class = CommissionSerializer
   permission_classes = [permissions.IsAuthenticated]


class HotDealViewSet(viewsets.ModelViewSet):
    queryset = HotDeal.objects.all()
    serializer_class = HotDealSerializer
    permission_classes = [permissions.IsAuthenticated]





# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import CustomTokenObtainPairSerializer

# class CustomLoginView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer


from rest_framework import viewsets
from .models import PublicProfile
from .serializers import PublicProfileSerializer

class PublicProfileViewSet(viewsets.ModelViewSet):
    queryset = PublicProfile.objects.all()
    serializer_class = PublicProfileSerializer




from rest_framework import viewsets
from .models import MyReels
from .serializers import MyReelsSerializer

class MyReelsViewSet(viewsets.ModelViewSet):
    queryset = MyReels.objects.all().order_by('-id')
    serializer_class = MyReelsSerializer

