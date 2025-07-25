from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseRedirect

from users.models import Company, Customer, User

from .models import Service, ServiceHistory
from .forms import CreateNewService, RequestServiceForm
from decimal import Decimal


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


def create(request):
    choices = [(field, field) for field, _ in Service._meta.get_field('field').choices]

    if request.method == 'POST':
        form = CreateNewService(request.POST, choices=choices)
        if form.is_valid():
            # Manually create a Service instance
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price_hour = form.cleaned_data['price_hour']
            field = form.cleaned_data['field']

            service = Service(
                name=name,
                description=description,
                price_hour=price_hour,
                field=field,
                company=request.user.company  # Assumes the user is a company
            )
            service.save()

            # Redirect to the service detail view
            return redirect('index', id=service.id)
    else:
        form = CreateNewService(choices=choices)

    return render(request, 'services/create.html', {'form': form})




def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


def request_service(request, id):
    service = get_object_or_404(Service, id=id)

    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            # Create a new service request (example assumes you have a ServiceHistory model)
            ServiceHistory.objects.create(
                customer=request.user.customer,# Assuming the user is a customer
                service=service,
                address=form.cleaned_data['address'],
                service_hours=form.cleaned_data['service_hours'],
                price=service.price_hour * Decimal(str(form.cleaned_data['service_hours']))
            )
            return redirect('customer_profile', username=request.user.username)
    else:
        form = RequestServiceForm()

    return render(request, 'services/request_service.html', {
        'form': form,
        'service': service,
    })
