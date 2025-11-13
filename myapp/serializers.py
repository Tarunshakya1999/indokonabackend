from rest_framework import serializers
from .models import Hero, ROLE_CHOICES ,PDF
from django.contrib.auth.models import User
from myapp.models import *



class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hero
        fields = '__all__'


class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF
        fields = '__all__'
# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    service = serializers.ChoiceField(choices=Profile.SERVICE_CHOICES, required=True)
    role = serializers.CharField(required=False, allow_blank=True, allow_null=True)  

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'service', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists."})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})

        service = data.get('service')
        role = data.get('role')

        # ✅ Make role mandatory only for Fintech & Store
        services_require_role = ['Fintech', 'Store']
        if service in services_require_role and not role:
            raise serializers.ValidationError({"role": "Role is required for this service."})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        service = validated_data.pop('service')
        role = validated_data.pop('role', None)  # ✅ handle optional role

        user = User.objects.create_user(**validated_data, password=password)

        user.profile.service = service
        user.profile.role = role if role else None  # ✅ save only if available
        user.profile.save()

        return user

from rest_framework import serializers
from .models import Plan, Testimonial, FAQ

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalProducts
        fields = '__all__'



class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=DigitalProducts.objects.all(), write_only=True, source='product'
    )

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_id', 'quantity']
        read_only_fields = ['user']



class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'


# serializers.py
from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
     model = Blog
     fields = '__all__'



# NEW SERIALIZERS


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Product, Order, Lead, Wallet, Commission, HotDeal


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id','username','email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
     model = Profile
     fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
     model = Product
     fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order
    fields = '__all__'


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
     model = Lead
     fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
   class Meta:
    model = Wallet
    fields = '__all__'


class CommissionSerializer(serializers.ModelSerializer):
   class Meta:
    model = Commission
    fields = '__all__'


class HotDealSerializer(serializers.ModelSerializer):
  class Meta:
   model = HotDeal
   fields = '__all__'


from rest_framework import serializers
from .models import PublicProfile, MyReels


# ✅ Public Profile Serializer
class PublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicProfile
        fields = '__all__'
        read_only_fields = ['is_varied', 'created_at']

    def validate_email(self, value):
        if PublicProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists. Please use a different one.")
        return value

    def validate_phone(self, value):
        if PublicProfile.objects.filter(phone=value).exists():
            raise serializers.ValidationError("This phone number already exists. Please use a different one.")
        return value

    def validate_aadhar_number(self, value):
        if PublicProfile.objects.filter(aadhar_number=value).exists():
            raise serializers.ValidationError("This Aadhar number already exists. Please use a different one.")
        return value


# ✅ My Reels Serializer
class MyReelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyReels
        fields = '__all__'
