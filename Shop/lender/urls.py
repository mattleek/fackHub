
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('become-lender/', views.become_lender, name='become_lender'),
    path('lender-admin/', views.lender_admin, name='lender_admin'),
    path('add-product/', views.add_product, name='add_product'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='lender/login.html'), name='login'),

]