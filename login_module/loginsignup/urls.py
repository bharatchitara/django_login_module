
from django.urls import path,include
from loginsignup import views

urlpatterns = [
    path('createuser',views.createUser),
    
    
]