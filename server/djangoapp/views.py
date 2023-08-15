from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'djangoapp/login.html')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    messages.info(request, 'Logged out successfully!')
    return redirect('home')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        messages.success(request, 'Account created successfully!')
        return redirect('login')
    return render(request, 'djangoapp/registration.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    dealers = [
        {'id': 1, 'name': 'Dealer 1', 'rating': 4.5},
        {'id': 2, 'name': 'Dealer 2', 'rating': 3.8},
        # Add more dealers as needed
    ]
    context = {'dealers': dealers}
    return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    # Get dealer details and reviews using dealer_id
    dealer = {'id': dealer_id, 'name': 'Dealer Name', 'rating': 4.2}
    reviews = [
        {'user': 'User 1', 'rating': 4, 'comment': 'Great experience!'},
        {'user': 'User 2', 'rating': 3, 'comment': 'Could be better.'},
        # Add more reviews as needed
    ]
    context = {'dealer': dealer, 'reviews': reviews}
    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "POST":
        user = request.user.username  # Assuming user is authenticated
        rating = int(request.POST['rating'])
        comment = request.POST['comment']
        # Save the review to the database or perform other actions
        messages.success(request, 'Review added successfully!')
        return redirect('dealer_details', dealer_id=dealer_id)
    return render(request, 'djangoapp/add_review.html')
