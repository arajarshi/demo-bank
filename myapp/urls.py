from .views import register , login , deposit , withdraw , home , balance ,transfer
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('deposit/',deposit,name='deposit'),
    path('withdraw/',withdraw,name='withdraw'),
    path('home/',home,name='home'),
    path('balance/',balance,name='balance'),
    path('transfer/',transfer,name='transfer')
]