from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Hero(models.Model):
    name = models.TextField()
    image = models.ImageField(upload_to="logo")
    tagline = models.TextField()
    supportline = models.TextField()

    def __str__(self):
        return self.name
    
ROLE_CHOICES = [
    ('Retailer', 'Retailer'),
    ('Distributor', 'Distributor'),
    ('Master Distributor', 'Master Distributor'),
    ('Admin', 'Admin'),
]


class Plan(models.Model):
    type = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to="plans", null=True, blank=True)
    setup = models.CharField(max_length=50, null=True, blank=True)
    renewal = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.type or "Plan"


# models.py
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    message = models.TextField()
    videos = models.FileField(upload_to="videos", null=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)  # 1 to 5 rating
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # ✅ Auto timestamp

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question
    
class PDF(models.Model):
    # ✅ Fix: Allowing the field to be NULL in the database
    name = models.TextField(null=True, blank=True)
    pdf = models.FileField(upload_to="pdf")

    def __str__(self):
        # Best practice: Ensure str() doesn't return None if name is null
        return self.name or f"PDF ID: {self.id}"
    


class DigitalProducts(models.Model):
    productname = models.TextField()
    productdescription = models.TextField()
    productprice = models.IntegerField()
    productdiscounted_price = models.IntegerField()
    productimg = models.ImageField(upload_to="uploadimage")
    productrating = models.PositiveSmallIntegerField(default=5) 

    def __str__(self):
        return self.productname
    


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(DigitalProducts, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.productname}"



from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="blogs/") # or URLField if using links
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.title

