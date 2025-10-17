from rest_framework import viewsets
from .models import *
from .serializers import *
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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

@csrf_exempt
def contact_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        message = data.get("message")

        # Save to DB
        ContactMessage.objects.create(
            name=name, email=email, phone=phone, message=message
        )

        # Send email
        subject = f"New Contact Message from {name}"
        body = f"""
        You have received a new message:
        Name: {name}
        Email: {email}
        Phone: {phone}
        Message: {message}
        """
        send_mail(
            subject,
            body,
            'shakyatarun32@gmail.com',  # sender
            ['shakyatarun32@gmail.com'],  # receiver (admin)
            fail_silently=False,
        )

        return JsonResponse({"success": "Message sent successfully!"})

    return JsonResponse({"error": "Invalid request"}, status=400)


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
    permission_classes = [permissions.IsAuthenticated]
    
class CartAPI(viewsets.ModelViewSet):
    queryset = Cart.objects.all()  # ✅ Add this
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


