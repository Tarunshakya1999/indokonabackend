from rest_framework import viewsets
from .models import Hero
from .serializers import HeroSerializer

class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.serializers import UserRegisterSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    

