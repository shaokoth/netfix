from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, TemplateView
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from services.models import ServiceHistory, Service
from django.shortcuts import render, redirect,get_object_or_404



from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer

@csrf_protect
def register(request):
    return render(request, 'users/register.html')

class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'users/register_customer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'users/register_company.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')
    


def LoginUserView(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    form.add_error(None, "Invalid email or password.")
            except User.DoesNotExist:
                form.add_error(None, "No user found with this email.")
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {"form": form})

@login_required
def CustomerProfileView(request, username):
    customer = Customer.objects.get(user=request.user)
    user_age = timezone.now().year - customer.birth.year
    requested_services = ServiceHistory.objects.filter(customer=customer).order_by('-request_date')
    return render(request, 'users/profile.html', {
        'user': request.user,
        'user_age': user_age,
        'sh': requested_services  # Placeholder for requested services history
    })

@login_required
def CompanyProfileView(request, username):
    company = get_object_or_404(Company, user__username=username)
    services = Service.objects.filter(company=company).order_by("-date")

    return render(request, 'users/profile.html', {
        'user': request.user,
        'company': company,
        'services': services,  # Pass the company's services to the template
    })