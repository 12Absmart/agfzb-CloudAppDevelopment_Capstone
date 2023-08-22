from django.db import models
from django.utils.timezone import now

# Create a Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # You can add more fields here

    def __str__(self):
        return self.name

# Create a Car Model model
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.CharField(max_length=50)  # Assuming dealer_id is a string
    CAR_TYPES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more choices here
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES)
    year = models.DateField()
    # You can add more fields here

    def __str__(self):
        return self.name

# Create a plain Python class CarDealer
class CarDealer:
    def __init__(self, dealer_id, name, address, city, state, zip_code):
        self.dealer_id = dealer_id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

# Create a plain Python class DealerReview
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
