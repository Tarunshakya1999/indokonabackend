from django.contrib import admin
from myapp.models import *


# Register your models here.
admin.site.register(Hero)
admin.site.register(Plan)
admin.site.register(Testimonial)
admin.site.register(FAQ)
admin.site.register(PDF)
admin.site.register(DigitalProducts)
admin.site.register(Cart)
admin.site.register(ContactMessage)
admin.site.register(Blog)
admin.site.register(MyReels)
admin.site.register(UsefulLink)
admin.site.register(MyPosts)
# admin.site.register(MSMERegistration)



# ✅ Wallet Admin
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'pending')
    search_fields = ('user__username',)


# ✅ Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# ✅ Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'product_type', 'category', 'active', 'created_at')
    list_filter = ('product_type', 'active', 'category')
    search_fields = ('title', 'slug')
    prepopulated_fields = {"slug": ("title",)} # auto generate slug


# ✅ Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'amount', 'status', 'transaction_id', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'product__title', 'transaction_id')


# ✅ Commission Admin
@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('product', 'percent', 'reseller')
    list_filter = ('percent',)
    search_fields = ('product__title', 'reseller__username')


# ✅ Lead Admin
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'source', 'status', 'assigned_to', 'created_at')
    list_filter = ('source', 'status')
    search_fields = ('name', 'phone', 'email', 'assigned_to__username')


# ✅ Hot Deals Admin
@admin.register(HotDeal)
class HotDealAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_price', 'start', 'end', 'active')
    list_filter = ('active',)
    search_fields = ('product__title',)



from django.contrib import admin
from .models import PublicProfile

@admin.register(PublicProfile)
class PublicProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "pincode", "is_varied", "created_at")
    list_filter = ("is_varied", "created_at")
    search_fields = ("name", "email", "phone", "aadhar_number")
    readonly_fields = ("created_at",)
    list_editable = ("is_varied",)



from django.contrib import admin
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from .models import MSMERegistration
import os
from django.conf import settings


@admin.action(description="📄 Download Selected MSME Data as PDF")
def export_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="msme_data.pdf"'

    p = canvas.Canvas(response)
    y = 820

    for obj in queryset:

        # ------- ALL TEXT FIELDS -------
        fields = [
            ("Full Name", obj.full_name),
            ("Mobile Number", obj.mobile_number),
            ("Email", obj.email),
            ("Aadhaar Number", obj.aadhaar_number),
            ("Applicant Type", obj.applicant_type),
            ("Business Name", obj.business_name),
            ("Business Address", obj.business_address),
            ("State", obj.state),
            ("District", obj.district),
            ("PIN Code", obj.pincode),
            ("Business Type", obj.business_type),
            ("Date of Starting", str(obj.date_of_starting)),
            ("PAN Number", obj.pan_number),
            ("Bank Account", obj.bank_account_number),
            ("IFSC Code", obj.ifsc_code),
            ("Employees", str(obj.number_of_employees)),
            ("Investment", obj.investment_in_plant_machinery),
            ("Annual Turnover", obj.annual_turnover),
            ("Created At", str(obj.created_at)),
        ]

        for label, value in fields:
            p.drawString(40, y, f"{label}: {value}")
            y -= 20

            if y < 100:
                p.showPage()
                y = 820

        # ------- Aadhaar Front Image -------
        if obj.aadhaar_front:
            img_path = os.path.join(settings.MEDIA_ROOT, obj.aadhaar_front.name)
            if os.path.exists(img_path):
                p.drawString(40, y, "Aadhaar Front:")
                y -= 160
                p.drawImage(ImageReader(img_path), 40, y, width=250, height=150)
                y -= 20

        # ------- Aadhaar Back Image -------
        if obj.aadhaar_back:
            img_path = os.path.join(settings.MEDIA_ROOT, obj.aadhaar_back.name)
            if os.path.exists(img_path):
                p.drawString(40, y, "Aadhaar Back:")
                y -= 160
                p.drawImage(ImageReader(img_path), 40, y, width=250, height=150)
                y -= 20

        # ------- Business Proof Image -------
        if obj.business_proof:
            img_path = os.path.join(settings.MEDIA_ROOT, obj.business_proof.name)
            if os.path.exists(img_path):
                p.drawString(40, y, "Business Proof:")
                y -= 160
                p.drawImage(ImageReader(img_path), 40, y, width=250, height=150)
                y -= 20

        # New Page for next record
        p.showPage()
        y = 820

    p.save()
    return response



@admin.register(MSMERegistration)
class MSMEAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MSMERegistration._meta.fields]
    actions = [export_pdf]



from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import os

from .models import FssaiRegistration


@admin.action(description="Download selected FSSAI records as PDF")
def download_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="fssai_records.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 50

    for obj in queryset:

        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, y, "FSSAI Registration Record")
        y -= 30

        p.setFont("Helvetica", 12)

        # -------- TEXT FIELDS ----------
        fields_to_show = [
            ("Applicant Name", obj.applicant_name),
            ("Business Name", obj.business_name),
            ("Address", obj.address),
            ("Business Type", obj.business_type),
            ("Turnover", obj.turnover),
            ("Processing", obj.processing),
            ("Created At", obj.created_at.strftime("%d-%m-%Y %H:%M")),
        ]

        for label, value in fields_to_show:
            p.drawString(50, y, f"{label}: {value}")
            y -= 22

            if y < 120:
                p.showPage()
                y = height - 50

        # ---------- IMAGES (photo + aadhar) ----------
        def draw_image(title, img_field):
            nonlocal y
            if img_field:
                img_path = os.path.join(settings.MEDIA_ROOT, img_field.name)
                if os.path.exists(img_path):
                    p.setFont("Helvetica-Bold", 12)
                    p.drawString(50, y, f"{title}:")
                    y -= 10
                    p.drawImage(ImageReader(img_path), 50, y - 180, width=200, height=180)
                    y -= 200

        draw_image("Applicant Photo", obj.photo)
        draw_image("Aadhar Image / PDF", obj.aadhar)

        # ---------- OTHER FILES (PDF / DOC / IMAGES) ----------
        def draw_file(title, file_field):
            nonlocal y
            if file_field:
                p.setFont("Helvetica-Bold", 12)
                p.drawString(50, y, f"{title}: {file_field.name}")
                y -= 20

        draw_file("Shop Document", obj.shop_docs)
        draw_file("Layout Document", obj.layout)

        # New page for next record
        p.showPage()
        y = height - 50

    p.save()
    return response


class FssaiAdmin(admin.ModelAdmin):
    list_display = ("id", "applicant_name", "business_name", "turnover", "created_at")
    actions = [download_pdf]


admin.site.register(FssaiRegistration, FssaiAdmin)
