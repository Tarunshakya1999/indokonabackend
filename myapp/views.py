from rest_framework import viewsets
from .models import *
from .serializers import *
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.serializers import UserRegisterSerializer

class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
    permission_classes = [AllowAny]



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


from rest_framework import viewsets
from .models import Plan, Testimonial, FAQ
from .serializers import PlanSerializer, TestimonialSerializer, FAQSerializer

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


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
   serializer_class = ProductSerializer2  
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

# myapp/views.py
from rest_framework import viewsets, permissions
from .models import PublicProfile
from .serializers import PublicProfileSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # requires that PublicProfile.user is set to request.user during creation
        return obj.user == request.user

class PublicProfileViewSet(viewsets.ModelViewSet):
    queryset = PublicProfile.objects.all()
    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # attach currently logged-in user
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # restrict list to current user's profile(s)
        user = self.request.user
        return PublicProfile.objects.filter(user=user)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated, IsOwner])
    def assets(self, request, pk=None):
        profile = self.get_object()
        assets = getattr(profile, "assets", None)
        if not assets:
            return Response({"detail":"No assets yet"}, status=404)
        from .serializers import ProfileAssetsSerializer
        return Response(ProfileAssetsSerializer(assets, context={"request": request}).data)



class MyReelsViewSet(viewsets.ModelViewSet):
    queryset = MyReels.objects.all().order_by('-id')
    serializer_class = MyReelsSerializer




class MypostViewSet(viewsets.ModelViewSet):
    queryset = MyPosts.objects.all().order_by('-id')
    serializer_class = MyPostSerializer




from rest_framework import viewsets
from .models import UsefulLink
from .serializers import UsefulLinkSerializer

class UsefulLinkViewSet(viewsets.ModelViewSet):
    queryset = UsefulLink.objects.all().order_by("-id")
    serializer_class = UsefulLinkSerializer





class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("id")
    serializer_class = CommentSerializer

    # 🔥 Filter comments by post ID → /api/comments/?post=2
    def get_queryset(self):
        qs = super().get_queryset()
        post_id = self.request.query_params.get("post")
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs
    


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response({"error": "All fields are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return Response({"message": "User registered successfully"}, status=201)








from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class CustomLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # User check
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid username or password"}, status=400)

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username,   # extra data (you wanted this)
            "email": user.email
        }, status=200)





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import MSMERegistrationSerializer

class MSMERegisterView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.AllowAny]  # change as needed

    def post(self, request, format=None):
        serializer = MSMERegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Saved"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework import viewsets
from .models import FssaiRegistration
from .serializers import FssaiRegistrationSerializer

class FssaiRegistrationViewSet(viewsets.ModelViewSet):
    queryset = FssaiRegistration.objects.all().order_by("-id")
    serializer_class = FssaiRegistrationSerializer



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Trademark
from .serializers import TrademarkSerializer

class TrademarkView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = TrademarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Trademark Submitted Successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status
# from django.core.mail import send_mail
# from .models import Contact
# from .serializers import ContactSerializer
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.permissions import AllowAny
# from rest_framework.decorators import api_view, permission_classes


# @api_view(['POST'])
# @csrf_exempt
# @permission_classes([AllowAny])
# def contact_api(request):
#     serializer = ContactSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()

#         # Email Send
#         name = serializer.data["name"]
#         email = serializer.data["email"]
#         phone = serializer.data["phone"]
#         service = serializer.data["service"]
#         message = serializer.data["message"]

#         subject = f"New Contact Form Submission - {name}"
#         body = f"""
#         Name: {name}
#         Email: {email}
#         Phone: {phone}
#         Service: {service}

#         Message:
#         {message}
#         """

#         send_mail(
#             subject,
#             body,
#             "shakyatarun32@gmail.com",      # FROM
#             ["shakyatarun32@gmail.com"],    # TO
#             fail_silently=False,
#         )

#         return Response({"message": "Message sent successfully!"}, status=status.HTTP_200_OK)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    

