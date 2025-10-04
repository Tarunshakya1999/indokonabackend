"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings  
from django.conf.urls.static import static 
from myapp.views import *
from django.urls import path
from myapp.views import *
from rest_framework_simplejwt.views import(
    TokenObtainPairView,TokenRefreshView

)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),
    path('api/register/', RegisterView.as_view(), name='register'),
   # path('get-role/', get_user_role),
    path('login/',TokenObtainPairView.as_view(),name="login"),
    path('api/token/referesh/',TokenRefreshView.as_view(),name="referesh3"),
    path("api/contact/", contact_view, name="contact"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


