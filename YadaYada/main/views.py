from django.shortcuts import render, redirect
from .forms import BasicForm
from django.http import HttpResponseRedirect
from .models import UserInfo, LocalUser  # Add LocalUser model
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = BasicForm(request.POST)
        if form.is_valid():
            UserInfo.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            return render(request, 'main/success.html', {'form': form})
    else:
        form = BasicForm()
    return render(request, 'main/home.html', {'form': form})

def landing_page(request):
    if request.method == 'POST':
        form = BasicForm(request.POST)
        if form.is_valid():
            UserInfo.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            return render(request, 'main/success.html', {'form': form})
    else:
        form = BasicForm()
    return render(request, 'main/landing.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = LocalUser.objects.get(email=email)
            if user.password == password:
                request.session['user_id'] = user.id  # Set session
                return redirect('loggedin')
            else:
                return render(request, 'main/login.html', {'error': 'Invalid email or password.'})
        except LocalUser.DoesNotExist:
            return render(request, 'main/login.html', {'error': 'Invalid email or password.'})
    return render(request, 'main/login.html')

def loggedin(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login_page')
    user = LocalUser.objects.get(id=user_id)
    return render(request, 'main/loggedin.html', {'user': user})

def loggedin_page(request):
    return render(request, 'main/success.html', {'message': 'You are now logged in!'})

def register_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            return render(request, 'main/register.html', {'error': 'Email and password are required.'})
        try:
            user = LocalUser.objects.create(email=email, password=password)
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login_page')
        except IntegrityError:
            return render(request, 'main/register.html', {'error': 'Email already exists.'})
    return render(request, 'main/register.html')

def itinerary_page(request):
    if request.method == 'POST':
        # Save booking info to database
        destination = request.POST.get('destination')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        guests = request.POST.get('guests')
        user_id = request.session.get('user_id')
        from .models import Booking, LocalUser
        if user_id:
            user = LocalUser.objects.get(id=user_id)
            Booking.objects.create(
                user=user,
                destination=destination,
                checkin=checkin,
                checkout=checkout,
                guests=guests if guests.isdigit() else 5
            )
        # Example itineraries (in real app, generate dynamically)
        itineraries = [
            {'title': 'Relaxing Beach Getaway', 'details': '3 nights at a 4-star resort, daily breakfast, airport transfer.'},
            {'title': 'Adventure & Culture', 'details': '2 nights city tour, 1 night hiking, museum tickets included.'},
            {'title': 'Family Fun', 'details': '4 nights family suite, theme park tickets, kids activities.'},
        ]
        return render(request, 'main/itinerary.html', {'itineraries': itineraries, 'destination': destination})
    return redirect('loggedin')
