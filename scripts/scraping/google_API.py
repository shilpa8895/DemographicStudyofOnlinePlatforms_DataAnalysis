import requests
import pandas as pd
import numpy as np
from scripts.scraping.youtube_config import API_KEY, CENTER_LAT, CENTER_LNG, STEP, NUM_STEPS

def generate_grid(center_lat, center_lng, step, num_steps):
    lat_change = np.linspace(-step * num_steps, step * num_steps, num_steps * 2 + 1)
    lng_change = np.linspace(-step * num_steps, step * num_steps, num_steps * 2 + 1)
    locations = [(center_lat + lat, center_lng + lng) for lat in lat_change for lng in lng_change]
    return locations

def fetch_place_details(api_key, place_id, fetched_ids):
    if place_id in fetched_ids:
        return None
    fetched_ids.add(place_id)
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'fields': 'name,formatted_address,place_id,international_phone_number,website,rating,review,price_level,types,geometry,reviews,business_status,opening_hours,photos',
        'key': api_key
    }
    response = requests.get(details_url, params=params)
    details = response.json().get('result', {})
    reviews = details.get('reviews', [])
    photos = details.get('photos', [])
    photo_urls = [f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo['photo_reference']}&key={api_key}" for photo in photos]
    opening_hours = details.get('opening_hours', {}).get('weekday_text', [])
    review_details = [f"{review['author_name']}: {review['text']}" for review in reviews]
    return {
        'Name': details.get('name', ''),
        'Address': details.get('formatted_address', ''),
        'Place ID': details.get('place_id', ''),
        'Phone Number': details.get('international_phone_number', ''),
        'Website': details.get('website', ''),
        'Rating': details.get('rating', ''),
        'Price Level': details.get('price_level', ''),
        'Types': ', '.join(details.get('types', [])),
        'Latitude': details.get('geometry', {}).get('location', {}).get('lat', ''),
        'Longitude': details.get('geometry', {}).get('location', {}).get('lng', ''),
        'Business Status': details.get('business_status', 'Not Available'),
        'Opening Hours': ', '.join(opening_hours),
        'Photo URLs': ', '.join(photo_urls),
        'Reviews': ' | '.join(review_details)
    }

def fetch_places(api_key, locations, search_query):
    """Fetches places from Google Places API using Text Search for a specific business name."""
    place_details_list = []
    fetched_ids = set()
    for (lat, lng) in locations:
        search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': f"{search_query} near {lat},{lng}",
            'key': api_key
        }
        response = requests.get(search_url, params=params)
        results = response.json().get('results', [])
        for result in results:
            place_id = result.get('place_id')
            details = fetch_place_details(api_key, place_id, fetched_ids)
            if details:
                place_details_list.append(details)
    return place_details_list

def main(api_key, center_lat, center_lng, step, num_steps):
    locations = generate_grid(center_lat, center_lng, step, num_steps)
    search_query = "Australia Post"
    place_details = fetch_places(api_key, locations, search_query)
    df = pd.DataFrame(place_details)
    return df

# Execute and save to Excel
place_details_df = main(API_KEY, CENTER_LAT, CENTER_LNG, STEP, NUM_STEPS)
excel_path = 'Australia_Post.xlsx'
place_details_df.to_excel(excel_path, index=False)