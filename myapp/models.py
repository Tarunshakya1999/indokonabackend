from django.db import models

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

from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=100)
    setup_cost = models.CharField(max_length=50)
    renewal = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    message = models.TextField()

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
