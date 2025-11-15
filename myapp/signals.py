# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()





# myapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PublicProfile, ProfileAssets
from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
import os

# helper to ensure assets exist
def ensure_assets_for_profile(profile):
    assets, created = ProfileAssets.objects.get_or_create(profile=profile)
    return assets

@receiver(post_save, sender=PublicProfile)
def generate_assets(sender, instance: PublicProfile, created, **kwargs):
    # only generate when profile is created OR when certain fields changed
    # for simplicity we generate on every save (but you can guard)
    assets = ensure_assets_for_profile(instance)

    # ---------- 1) Generate Certificate (PDF) using ReportLab ----------
    try:
        buffer = BytesIO()
        # landscape A4 certificate
        c = canvas.Canvas(buffer, pagesize=landscape(A4))
        width, height = landscape(A4)

        # background / border
        c.setStrokeColorRGB(0.1, 0.3, 0.6)
        c.setLineWidth(4)
        c.rect(40, 40, width-80, height-80, stroke=1, fill=0)

        # Title
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(width/2, height - 140, "Certificate of Profile")

        # Name
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(width/2, height - 220, instance.name)

        # Details block
        c.setFont("Helvetica", 14)
        text = f"Email: {instance.email}    |    Phone: {instance.phone}    |    DOB: {instance.dob or 'N/A'}"
        c.drawCentredString(width/2, height - 260, text)

        # Address
        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, height - 290, f"Address: {instance.address}")

        # Footer
        c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(width/2, 60, f"Generated on: {instance.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        c.showPage()
        c.save()
        pdf = buffer.getvalue()
        buffer.close()

        # Save to FileField if different or empty
        file_name = f"certificate_{instance.id}.pdf"
        assets.certificate.save(file_name, ContentFile(pdf), save=False)
    except Exception as e:
        # log if needed
        print("Certificate generation error:", e)

    # ---------- 2) Generate ID card (small PNG) using Pillow ----------
    try:
        W, H = (600, 360)  # id card size
        img = Image.new("RGB", (W, H), color=(255,255,255))
        draw = ImageDraw.Draw(img)

        # Basic fonts - in production give full path to TTF
        try:
            font_name = ImageFont.truetype("arial.ttf", 28)
            font_small = ImageFont.truetype("arial.ttf", 16)
        except:
            font_name = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # left rectangle for photo
        draw.rectangle([20, 20, 160, 320], fill=(230,230,230))
        # paste profile picture scaled if exists
        if instance.userpic:
            try:
                profile_img = Image.open(instance.userpic.path).convert("RGB")
                profile_img.thumbnail((130, 300))
                px = 20 + (140 - profile_img.width)//2
                py = 20 + (300 - profile_img.height)//2
                img.paste(profile_img, (px, py))
            except Exception as e:
                print("Profile pic paste fail:", e)

        # Name and details
        draw.text((180, 40), instance.name, font=font_name, fill=(10,10,10))
        draw.text((180, 90), f"Phone: {instance.phone}", font=font_small, fill=(50,50,50))
        draw.text((180, 120), f"Email: {instance.email}", font=font_small, fill=(50,50,50))
        draw.text((180, 150), f"Address: {instance.address[:40]}...", font=font_small, fill=(50,50,50))
        draw.text((180, 200), f"Aadhaar: {instance.aadhar_number}", font=font_small, fill=(50,50,50))

        # Save to bytes
        bio = BytesIO()
        img.save(bio, format="PNG")
        bio.seek(0)
        assets.id_card.save(f"idcard_{instance.id}.png", ContentFile(bio.read()), save=False)
        bio.close()
    except Exception as e:
        print("ID card generation error:", e)

    # ---------- 3) Generate Visiting card (simple) ----------
    try:
        W, H = (1000, 600)
        card = Image.new("RGB", (W, H), color=(255,255,255))
        d = ImageDraw.Draw(card)
        try:
            big = ImageFont.truetype("arial.ttf", 48)
            mid = ImageFont.truetype("arial.ttf", 22)
        except:
            big = ImageFont.load_default()
            mid = ImageFont.load_default()

        # Left colored block
        d.rectangle([0,0,300,H], fill=(13,110,253))
        # User name on left block
        d.text((30, 200), instance.name, font=big, fill=(255,255,255))

        # Right details
        d.text((340, 120), f"Phone: {instance.phone}", font=mid, fill=(0,0,0))
        d.text((340, 160), f"Email: {instance.email}", font=mid, fill=(0,0,0))
        d.text((340, 200), f"Address: {instance.address}", font=mid, fill=(0,0,0))
        d.text((340, 240), f"Aadhaar: {instance.aadhar_number}", font=mid, fill=(0,0,0))

        bio2 = BytesIO()
        card.save(bio2, format="PNG")
        bio2.seek(0)
        assets.visiting_card.save(f"visitingcard_{instance.id}.png", ContentFile(bio2.read()), save=False)
        bio2.close()
    except Exception as e:
        print("Visiting card generation error:", e)

    # Finally save assets record
    try:
        assets.save()
    except Exception as e:
        print("Saving assets failed:", e)

