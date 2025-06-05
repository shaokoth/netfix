from django.urls import path

from . import views as v

urlpatterns = [
    path('register/company/', v.CompanySignUpView.as_view(), name='register_company'),
    path('register/customer/', v.CustomerSignUpView.as_view(), name='register_customer'),
]
