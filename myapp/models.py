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
    productdescription = models.CharField(max_length=1000)
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
    



# New Models :  


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    is_reseller = models.BooleanField(default=False)
    kyc_submitted = models.BooleanField(default=False)
    payout_upi = models.CharField(max_length=100, blank=True)

    def __str__(self):
      return self.user.username





class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pending = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class Category(models.Model):
  name = models.CharField(max_length=120)

  def __str__(self):
   return self.name


class Product(models.Model):
   PRODUCT_TYPES = (( 'digital', 'Digital'), ('software','Software'), ('resale','Resale'))
   title = models.CharField(max_length=255)
   slug = models.SlugField(unique=True)
   description = models.TextField(blank=True)
   price = models.DecimalField(max_digits=10, decimal_places=2)
   product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default='digital')
   file_url = models.URLField(blank=True)
   category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
   active = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       return self.title
   



class Order(models.Model):
  STATUS = (('pending','Pending'),('paid','Paid'),('delivered','Delivered'),('refunded','Refunded'))
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  status = models.CharField(max_length=20, choices=STATUS, default='pending')
  transaction_id = models.CharField(max_length=255, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)




class Commission(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
  percent = models.DecimalField(max_digits=5, decimal_places=2, default=10)
  reseller = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)



class Lead(models.Model):
   SOURCE = (('facebook','Facebook'),('instagram','Instagram'),('website','Website'),('referral','Referral'))
   name = models.CharField(max_length=200)
   email = models.EmailField(blank=True)
   phone = models.CharField(max_length=30, blank=True)
   source = models.CharField(max_length=50, choices=SOURCE, default='website')
   status = models.CharField(max_length=50, default='new')
   assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_leads')
   notes = models.TextField(blank=True)
   created_at = models.DateTimeField(auto_now_add=True)



class HotDeal(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  discount_price = models.DecimalField(max_digits=10, decimal_places=2)
  start = models.DateTimeField()
  end = models.DateTimeField()
  active = models.BooleanField(default=True)


from django.db import models
from django.contrib.auth.models import User


# ✅ Profile Model (Role + Service)
class Profile(models.Model):
    SERVICE_CHOICES = [
        ('Fintech', 'Indokona Fintech'),
        ('Suit', 'Indokona Suite'),
        ('SaaS', 'Indokona SaaS'),
        ('M2M', 'Indokona M2M'),
        ('Store', 'Indokona Digital Store'),
        ('Acadmy', 'Indokona Academy'),
    ]

    ROLE_CHOICES = [
        # Fintech roles
        ('Retailer', 'Retailer'),
        ('Distributor', 'Distributor'),
        ('Master Distributor', 'Master Distributor'),
        ('Super Distributor', 'Super Distributor'),
        ('White Label', 'White Label'),

        # Store roles
        ('Basic Reseller', 'Basic Reseller'),
        ('Pro Reseller', 'Pro Reseller'),
        ('Gold Reseller', 'Gold Reseller'),
        ('Diamond Reseller', 'Diamond Reseller'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default=None, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# ✅ Reels Model
class MyReels(models.Model):
    author = models.TextField()
    caption = models.CharField(max_length=50)
    src = models.FileField(upload_to="reels")
    music = models.FileField(upload_to="music", blank=True, null=True)

    def __str__(self):
        return self.author


# ✅ Posts Model
class MyPosts(models.Model):
    author = models.TextField()
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="myposts")
    likes = models.IntegerField(default=0)
    time = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.author


# ✅ Public Profile Model
class PublicProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    userpic = models.ImageField(upload_to="public/")
    created_at = models.DateTimeField(auto_now_add=True)
    pincode = models.IntegerField()
    dob = models.DateField(null=True,blank=True)
    is_varied = models.BooleanField(default=False)
    aadhar_number = models.CharField(max_length=20, blank=False, null=False, unique=True)
    aadhar_card_pic = models.FileField(upload_to="aadhar/", blank=False, null=False)

    def __str__(self):
        return self.name
