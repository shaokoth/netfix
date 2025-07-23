from django.shortcuts import render

from users.models import User, Company
from services.models import Service, Customer,ServiceHistory
from django.shortcuts import get_object_or_404
from datetime import date


def home(request):
    return render(request, 'users/home.html', {'user': request.user})

def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def customer_profile(request, name):
    user = get_object_or_404(User, username=name, is_customer=True)
    customer = get_object_or_404(Customer, user=user)
    user_age = calculate_age(customer.birth) if customer.birth else 'N/A'
    sh = ServiceHistory.objects.filter(customer=customer).order_by("-date")

    return render(request, 'users/profile.html', {
        'user': user,
        'user_age': user_age,
        'sh': sh,
    })
    
    
def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = get_object_or_404(User, username=name)
    services = Service.objects.filter(
        company=Company.objects.get(user=user)).order_by("-date")

    return render(request, 'users/profile.html', {'user': user, 'services': services})
