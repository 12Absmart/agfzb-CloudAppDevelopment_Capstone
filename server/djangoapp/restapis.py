import requests
import json
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse
from .models import CarDealer, DealerReview


# Define global constants
API_KEY = 'klrYHIbvrBFwi-BzzoUYVVHMkVyg7GpIRiC5gpXMSm_y'
CF_BASE_URL = 'https://us-south.functions.appdomain.cloud/api/v1/web/f528e3f2-7dfd-470f-8566-800cb95418ac/dealership-package'

# Define get_request function
def get_request(url, params=None, headers=None, auth=None):
    response = requests.get(url, params=params, headers=headers, auth=auth)
    return response

# Define post_request function
def post_request(url, params=None, json_data=None):
    response = requests.post(url, params=params, json=json_data)
    return response


# Define get_dealers_from_cf function
def get_dealers_from_cf(url, **kwargs):
    results = []
    response = get_request(url, params=kwargs)
    
    if response.status_code == 200:
        json_result = response.json()
        dealers_data = json_result.get("dealerships", [])  # Change "rows" to "dealerships"
        
        for dealer_data in dealers_data:
            dealer_obj = CarDealer(
                address=dealer_data.get("address", ""),
                city=dealer_data.get("city", ""),
                full_name=dealer_data.get("full_name", ""),
                id=dealer_data.get("id", ""),
                lat=dealer_data.get("lat", ""),
                long=dealer_data.get("long", ""),
                short_name=dealer_data.get("short_name", ""),
                st=dealer_data.get("st", ""),
                zip=dealer_data.get("zip", "")
            )
            results.append(dealer_obj)
    
    return results





def get_dealerships(request):
    url = f'{CF_BASE_URL}/get-dealership'  # Replace with the correct route
    dealerships = []
    response = get_request(url)
    
    if response.status_code == 200:
        json_result = response.json()
        dealerships_data = json_result.get("rows", [])
        
        for dealer_data in dealerships_data:
            dealer_doc = dealer_data.get("doc", {})
            dealer_obj = {
                'id': dealer_doc.get("id", ""),
                'full_name': dealer_doc.get("full_name", ""),
                'city': dealer_doc.get("city", ""),
                'address': dealer_doc.get("address", ""),
                 'zip': dealer_doc.get("zip", ""),
                'st': dealer_doc.get("st", "")
            }
            dealerships.append(dealer_obj)
    
    return dealerships



# Define get_dealer_reviews_from_cf function
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    response = get_request(url, params={"dealerId": dealer_id})
    
    if response.status_code == 200:
        json_result = response.json()
        reviews_data = json_result.get("reviews", [])
        
        for review_data in reviews_data:
            review_obj = DealerReview(
                dealership=review_data.get("dealership", ""),
                name=review_data.get("name", ""),
                purchase=review_data.get("purchase", ""),
                review=review_data.get("review", ""),
                purchase_date=review_data.get("purchase_date", "")
            )
            results.append(review_obj)
    
    return results

# Define analyze_review_sentiments function
def analyze_review_sentiments(text):
    url = f'{CF_BASE_URL}/analyze-sentiment'  # Replace with the correct route
    payload = {'text': text}
    response = post_request(url, json_data=payload)
    
    if response.status_code == 200:
        sentiment_data = response.json()
        sentiment_label = sentiment_data.get('sentiment_label', 'Unknown')
        return sentiment_label
    else:
        return 'Unknown'

# Define get_dealerships view method
def get_dealerships(request):
    if request.method == "GET":
        url = f'{CF_BASE_URL}/get-dealership'  # Replace with the correct route
        dealerships = get_dealers_from_cf(url)
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return HttpResponse(dealer_names)
