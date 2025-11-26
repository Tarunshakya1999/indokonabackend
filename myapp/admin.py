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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings
import os

from .models import MSMERegistration


@admin.action(description="📄 Download Selected MSME Data as PDF")
def export_pdf(modeladmin, request, queryset):

    if queryset.count() != 1:
        return HttpResponse("Please select only one record.")

    obj = queryset.first()

    filename = f"MSME_{obj.id}.pdf"

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # ---------------------------
    # PDF TITLE
    # ---------------------------
    story.append(Paragraph("<b>MSME REGISTRATION DETAILS</b>", styles['Title']))
    story.append(Spacer(1, 20))

    # ---------------------------
    # TEXT FIELDS
    # ---------------------------
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
        ("Bank Account No.", obj.bank_account_number),
        ("IFSC Code", obj.ifsc_code),
        ("No. of Employees", str(obj.number_of_employees)),
        ("Investment in Plant/Machinery", obj.investment_in_plant_machinery),
        ("Annual Turnover", obj.annual_turnover),
        ("Created At", obj.created_at.strftime("%d-%m-%Y %H:%M")),
    ]

    for label, value in fields:
        story.append(Paragraph(f"<b>{label}:</b> {value}", styles["Normal"]))
        story.append(Spacer(1, 10))

    story.append(PageBreak())  # next page for images

    # ---------------------------
    # IMAGE FIELDS – Each on New Page
    # ---------------------------
    image_fields = [
        ("Aadhaar Front", obj.aadhaar_front),
        ("Aadhaar Back", obj.aadhaar_back),
        ("Business Proof", obj.business_proof),
    ]

    for title, filefield in image_fields:
        if filefield:
            file_path = os.path.join(settings.MEDIA_ROOT, filefield.name)

            story.append(Paragraph(f"<b>{title}</b>", styles["Heading2"]))
            story.append(Spacer(1, 20))

            if os.path.exists(file_path) and filefield.name.lower().endswith((".jpg", ".jpeg", ".png")):
                story.append(Image(file_path, width=400, height=500))

            else:
                story.append(Paragraph("Unable to load image", styles["Normal"]))

            story.append(PageBreak())

    doc.build(story)
    return response



@admin.register(MSMERegistration)
class MSMEAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MSMERegistration._meta.fields]
    actions = [export_pdf]
from django.contrib import admin
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from django.conf import settings
import os

from .models import FssaiRegistration


class FssaiRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "id", "applicant_name", "business_name", "address",
        "business_type", "turnover", "processing",
        "aadhar", "photo", "shop_docs", "layout",
        "created_at"
    )
    actions = ["download_selected_pdf"]

    def download_selected_pdf(self, request, queryset):
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=fssai_records.pdf"

        doc = SimpleDocTemplate(response, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        for obj in queryset:

            # -------------------------
            #   TITLE FOR EACH RECORD
            # -------------------------
            story.append(Paragraph("<b>FSSAI Registration Details</b>", styles["Title"]))
            story.append(Spacer(1, 15))

            # -------------------------
            #   TEXT FIELDS PRINTABLE
            # -------------------------
            for field in obj._meta.fields:
                value = getattr(obj, field.name)

                # File / Image → clickable link
                if hasattr(value, "url"):
                    file_url = request.build_absolute_uri(value.url)
                    story.append(Paragraph(
                        f"<b>{field.verbose_name}:</b> <a href='{file_url}'>{file_url}</a>",
                        styles["Normal"]
                    ))
                else:
                    story.append(Paragraph(
                        f"<b>{field.verbose_name}:</b> {value}",
                        styles["Normal"]
                    ))

                story.append(Spacer(1, 8))

            # Add page break before images
            story.append(PageBreak())

            # -------------------------
            #   IMAGE FIELDS SEPARATE PAGES
            # -------------------------

            image_fields = [
                ("Aadhaar", obj.aadhar),
                ("Photo", obj.photo),
                ("Shop Document", obj.shop_docs),
                ("Layout", obj.layout),
            ]

            for title, filefield in image_fields:
                if filefield:
                    file_path = os.path.join(settings.MEDIA_ROOT, filefield.name)

                    story.append(Paragraph(f"<b>{title}</b>", styles["Heading2"]))
                    story.append(Spacer(1, 20))

                    # Only load if it is image format   
                    if os.path.exists(file_path) and filefield.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        story.append(Image(file_path, width=400, height=480))
                    else:
                        story.append(Paragraph("File is not an image (showing only link above).", styles["Normal"]))

                    story.append(PageBreak())

        doc.build(story)
        return response

    download_selected_pdf.short_description = "Download selected records as PDF"


admin.site.register(FssaiRegistration, FssaiRegistrationAdmin)




from django.contrib import admin
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings
import os

from .models import Trademark


def download_as_pdf(modeladmin, request, queryset):
    if queryset.count() != 1:
        return HttpResponse("Please select only one record to download.")

    obj = queryset.first()

    # PDF filename
    filename = f"Trademark_{obj.id}.pdf"

    # Create HTTP Response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # ----------------------------------------
    #  Add all text fields
    # ----------------------------------------
    story.append(Paragraph("<b>Trademark Registration Details</b>", styles['Title']))
    story.append(Spacer(1, 20))

    fields = [
        ("Applicant Name", obj.applicant_name),
        ("Mobile Number", obj.mobile),
        ("Email", obj.email),
        ("Business Type", obj.business_type),
        ("Brand Name", obj.brand_name),
        ("Classes Selected", obj.classes),
        ("Activity Description", obj.business_activity),
        ("Address", obj.address),
        ("State", obj.state),
        ("Pincode", obj.pincode),
        ("Created At", obj.created_at.strftime("%d-%m-%Y %H:%M"))
    ]

    for label, value in fields:
        story.append(Paragraph(f"<b>{label}:</b> {value}", styles['Normal']))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # ----------------------------------------
    # File fields (Image + PDF)
    # ----------------------------------------
    file_fields = [
        ("Brand Logo", obj.brand_logo),
        ("Aadhaar", obj.aadhaar),
        ("PAN", obj.pan),
        ("Business Proof", obj.business_proof),
    ]

    for title, filefield in file_fields:
        if filefield:
            file_path = os.path.join(settings.MEDIA_ROOT, filefield.name)

            story.append(Paragraph(f"<b>{title}</b>", styles["Heading2"]))
            story.append(Spacer(1, 15))

            # Check if image
            if filefield.name.lower().endswith((".jpg", ".jpeg", ".png")):
                try:
                    story.append(Image(file_path, width=400, height=500))
                except:
                    story.append(Paragraph("Unable to load image", styles["Normal"]))
            else:
                # For PDF/other file: show file path
                story.append(Paragraph(f"File: {filefield.url}", styles["Normal"]))

            story.append(PageBreak())  # Each file separate page

    # Build PDF
    doc.build(story)
    return response


download_as_pdf.short_description = "Download Selected as PDF"

@admin.register(Trademark)
class TrademarkAdmin(admin.ModelAdmin):
    list_display = ("id", "applicant_name", "mobile", "email", "business_type")
    actions = [download_as_pdf]

