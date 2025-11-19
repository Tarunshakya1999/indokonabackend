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
