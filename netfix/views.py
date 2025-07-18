from django.shortcuts import render

from users.models import User, Company
from services.models import Service, ServiceHistory, Customer
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime, date


def home(request):
    return render(request, 'users/home.html', {'user': request.user})

def calculate_age(birthdate):
    today = date.today()
    return today.year - birthdate.year - (
        (today.month, today.day) < (birthdate.month, birthdate.day)
    )

def customer_profile(request):
    # fetches the customer user and all of the services requested by it
    # user = request.user
    # services = user.customer.servicehistory_set.all().order_by("-request_date")

    # return render(request, 'users/profile.html', {'user': user, 'services': services})
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # or a 403/404 page if preferred

    # Get the Customer instance
    customer = get_object_or_404(Customer, user=request.user)

    # Get the service history for this customer
    sh = ServiceHistory.objects.filter(user=customer).order_by('-request_date')
    user_age = calculate_age(customer.birthdate) if customer.birthdate else "N/A"

    return render(request, 'users/profile.html', {
        'user': request.user,
        'sh': sh,
        'user_age': user_age,
    })

def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = get_object_or_404(User, username=name)
    company = get_object_or_404(Company, user=user)
    services = Service.objects.filter(
        company=Company.objects.get(user=user)).order_by("-date")

    return render(request, 'users/profile.html', {'user': user, 'services': services})
