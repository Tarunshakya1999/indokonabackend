from rest_framework import viewsets
from .models import Hero
from .serializers import HeroSerializer
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



@csrf_exempt
def contact_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")
        number = data.get("phone")
        
        subject = f"New Contact Message from {name}"
        body = f"Name: {name}\nEmail: {email}\nPhone Number : {number}\nMessage: {message}"

        try:
            send_mail( 
                subject,
                body,
                "shakyatarun32@gmail.com",  
                ["shakyatarun32@gmail.com"], 
                fail_silently=False,
            )
            return JsonResponse({"status": "success", "msg": "Message sent successfully!"})
        except Exception as e:
            return JsonResponse({"status": "error", "msg": str(e)})
    return JsonResponse({"status": "error", "msg": "Invalid request"})


    

