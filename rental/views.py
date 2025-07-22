from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Booking, Profile
from .forms import BookingForm, UserRegistrationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from datetime import timedelta
from django.db.models import Q
from django.contrib.auth import login , logout

def home(request):
    cars = Car.objects.all
    return render(request, 'rental/home.html', {'cars': cars})

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'rental/car_list.html', {'cars': cars})

def about(request):
    return render(request, 'rental/about.html')

def contact(request):
    return render(request, 'rental/contact.html')

@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            rental_days = (form.cleaned_data['end_date'] - form.cleaned_data['start_date']).days
            if rental_days <= 0:
                form.add_error(None, "End date must be after start date.")
            else:
                booking.total_price = car.price_per_day * rental_days
            booking.save()
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()
        
    return render(request, 'rental/book_car.html', {'form': form, 'car': car})
    
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'rental/booking_confirmation.html', {'booking': booking})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Invalid credentials. Please register if you don't have an account.")
        return redirect('register')  # This redirects failed login attempts to the register page

def available_cars(start_date, end_date):
    return Car.objects.exclude(
        booking__start_date__lt = end_date,
        booking__end_date__gt = start_date
    )

@login_required
def user_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'rental/user_profile.html', {'profile': profile})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            return redirect('home')  # change 'home' to your desired landing page
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
        else:
            form = ProfileForm(instance=profile)
            return render(request, 'rental/edit_profile.html', {'form': form})

def custom_logout_view(request):
    logout(request)
    return redirect('home')
