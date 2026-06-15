"""
Data processing module - handles all calculations, filtering, and aggregation
of review data.

This module contains pure processing logic without any user input/output
or visualisation code.
"""

from collections import defaultdict
import csv
import json
import os

def filter_reviews_by_park(reviews, park_name):
    """
    Returns all reviews belonging to a specific Disneyland park.
    
    Args:
        reviews (list): List of review dictionaries
        park_name (str): Name of the park to filter by
    
    Returns:
        list: Filtered reviews for the specified park
    """
    return [review for review in reviews if review['branch'].lower() == park_name.lower()]

def count_reviews_by_park_and_location(reviews, park_name, location):
    """
    Counts how many reviews a specific park received from a given location.
    
    Args:
        reviews (list): List of review dictionaries
        park_name (str): Name of the park
        location (str): Reviewer's home location
    
    Returns:
        int: Number of matching reviews
    """
    park_reviews = filter_reviews_by_park(reviews, park_name)
    return len([review for review in park_reviews 
                if review['reviewer_location'].lower() == location.lower()])

def calculate_average_rating_by_park_and_year(reviews, park_name, year):
    """
    Calculates the average rating for a park in a specific year.
    
    Args:
        reviews (list): List of review dictionaries
        park_name (str): Name of the park
        year (int): Year to filter by
    
    Returns:
        float: Average rating rounded to 2 decimal places, or 0 if no reviews
    """
    park_reviews = filter_reviews_by_park(reviews, park_name)
    
    # Filter by year (extract year from Year_Month field)
    year_reviews = []
    for review in park_reviews:
        try:
            review_year = int(review['year_month'].split()[1])
            if review_year == year:
                year_reviews.append(review)
        except:
            continue
    
    if not year_reviews:
        return 0.0
    
    total_ratings = sum(review['rating'] for review in year_reviews)
    average = total_ratings / len(year_reviews)
    return round(average, 2)

def count_reviews_per_park(reviews):
    """
    Counts total reviews for each Disneyland park.
    
    Args:
        reviews (list): List of review dictionaries
    
    Returns:
        dict: Park names as keys, review counts as values
    """
    park_counts = defaultdict(int)
    for review in reviews:
        park_counts[review['branch']] += 1
    return dict(park_counts)

def calculate_average_rating_by_location(reviews, park_name):
    """
    Calculates average rating for a park, grouped by reviewer location.
    
    Args:
        reviews (list): List of review dictionaries
        park_name (str): Name of the park to analyse
    
    Returns:
        dict: Location as keys, average rating as values
    """
    park_reviews = filter_reviews_by_park(reviews, park_name)
    
    location_ratings = defaultdict(list)
    for review in park_reviews:
        location = review['reviewer_location']
        location_ratings[location].append(review['rating'])
    
    location_averages = {}
    for location, ratings in location_ratings.items():
        location_averages[location] = round(sum(ratings) / len(ratings), 2)
    
    return location_averages

def calculate_average_by_park_and_location(reviews):
    """
    For every park, calculates average rating from each reviewer location.
    
    Args:
        reviews (list): List of review dictionaries
    
    Returns:
        dict: Nested dictionary - park -> location -> average rating
    """
    all_parks = {}
    unique_parks = set(review['branch'] for review in reviews)
    
    for park in unique_parks:
        all_parks[park] = calculate_average_rating_by_location(reviews, park)
    
    return all_parks

def calculate_monthly_average_ratings(reviews, park_name):
    """
    Calculates average rating per month (across all years) for a specific park.
    
    Args:
        reviews (list): List of review dictionaries
        park_name (str): Name of the park to analyse
    
    Returns:
        dict: Month numbers (1-12) as keys, average ratings as values
    """
    park_reviews = filter_reviews_by_park(reviews, park_name)
    
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    month_ratings = defaultdict(list)
    
    for review in park_reviews:
        month_num = extract_month_number(review['year_month'])
        if month_num > 0:
            month_ratings[month_num].append(review['rating'])
    
    monthly_averages = {}
    for month_num in range(1, 13):
        if month_ratings[month_num]:
            avg = sum(month_ratings[month_num]) / len(month_ratings[month_num])
            monthly_averages[month_map[month_num]] = round(avg, 2)
        else:
            monthly_averages[month_map[month_num]] = 0.0
    
    return monthly_averages

def extract_month_number(year_month_string):
    """Helper function to extract month number from Year_Month field."""
    month_abbrev = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    try:
        month_part = year_month_string.split()[0]
        return month_abbrev.get(month_part, 0)
    except:
        return 0

def generate_park_summary(reviews):
    """
    Generates aggregate information for each park including:
    - Number of reviews
    - Number of positive reviews (rating >= 4)
    - Average review score
    - Number of unique countries/locations that reviewed each park
    
    Args:
        reviews (list): List of review dictionaries
    
    Returns:
        list: List of dictionaries, each containing summary data for a park
    """
    unique_parks = set(review['branch'] for review in reviews)
    summary_data = []
    
    for park in unique_parks:
        park_reviews = filter_reviews_by_park(reviews, park)
        
        total_reviews = len(park_reviews)
        positive_reviews = len([r for r in park_reviews if r['rating'] >= 4])
        avg_score = round(sum(r['rating'] for r in park_reviews) / total_reviews, 2)
        
        unique_locations = set(r['reviewer_location'] for r in park_reviews)
        country_count = len(unique_locations)
        
        summary_data.append({
            'park_name': park,
            'total_reviews': total_reviews,
            'positive_reviews': positive_reviews,
            'average_rating': avg_score,
            'unique_countries': country_count
        })
    
    return summary_data

def export_summary_data(summary_data, filename, file_format):
    """
    Exports park summary data to TXT, CSV, or JSON format.
    
    Args:
        summary_data (list): List of park summary dictionaries
        filename (str): Name of the file to create
        file_format (str): Format to export ('txt', 'csv', or 'json')
    
    Returns:
        bool: True if export successful, False otherwise
    """
    try:
        if file_format == 'txt':
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("DISNEYLAND PARKS SUMMARY REPORT\n")
                f.write("=" * 60 + "\n\n")
                
                for park in summary_data:
                    f.write(f"Park: {park['park_name']}\n")
                    f.write(f"  Total Reviews: {park['total_reviews']}\n")
                    f.write(f"  Positive Reviews (4+ stars): {park['positive_reviews']}\n")
                    f.write(f"  Average Rating: {park['average_rating']}/5.0\n")
                    f.write(f"  Unique Countries: {park['unique_countries']}\n")
                    f.write("-" * 40 + "\n")
                    
        elif file_format == 'csv':
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['park_name', 'total_reviews', 
                                                        'positive_reviews', 'average_rating', 
                                                        'unique_countries'])
                writer.writeheader()
                writer.writerows(summary_data)
                
        elif file_format == 'json':
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, indent=4, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f"Export error: {e}")
        return False