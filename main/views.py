from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from services.models import Service
from django.db.models import Count


def home(request):
    most_requested_services = Service.objects.annotate(
        request_count=Count('servicehistory')  # or 'histories' if you added related_name
    ).order_by('-request_count')[:3]

    context = {
        'most_requested_services': most_requested_services,
    }
    return render(request, 'main/home.html', context)

def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
