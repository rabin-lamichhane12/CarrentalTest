from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Booking, Profile
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from datetime import timedelta


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


@login_required
def user_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'rental/user_profile.html', {'profile': profile})