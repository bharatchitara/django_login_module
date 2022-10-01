from django.urls import path,include,re_path
from loginsignup import views

urlpatterns = [
    path('createuser',views.createUser),
    path('updateuser',views.updateUser),
    # re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.activate, name='activate')
    path('activate/<uidb64>/<token>/',  views.activate, name='activate'),
    path('deleteuser',views.deleteUser),
    
    path('login',views.login),
    
    
]