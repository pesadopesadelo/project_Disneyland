"""
Main program controller - handles the flow between user interface,
data processing, and visualisation modules.

This module orchestrates the entire application, managing menu navigation
and coordinating between different components without handling direct
user input or data processing logic.
"""
   
import tui
import process
import visual
import csv
from datetime import datetime

def load_review_data():
    """
    Reads the Disneyland reviews CSV file and converts it into a structured list.
    
    Returns:
        list: A list of dictionaries, each representing one review with keys:
              'review_id', 'rating', 'year_month', 'reviewer_location', 'branch'
    """
    reviews = []
    
    try:
        with open('Disneyland_reviews.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                review = {
                    'review_id': int(row['Review_ID']),
                    'rating': int(row['Rating']),
                    'year_month': row['Year_Month'],
                    'reviewer_location': row['Reviewer_Location'],
                    'branch': row['Branch']
                }
                reviews.append(review)
    except FileNotFoundError:
        tui.display_error_message("Data file not found! Please ensure Disneyland_reviews.csv is in the correct location.")
        return None
    
    return reviews

def extract_year_from_month(year_month_string):
    """Helper to extract year from Year_Month format."""
    try:
        return int(year_month_string.split()[1])
    except:
        return 0

def extract_month_from_date(year_month_string):
    """Helper to extract month name from Year_Month string."""
    month_map = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    try:
        month_abbr = year_month_string.split()[0]
        return month_map.get(month_abbr, 0)
    except:
        return 0

def run():
    """Main program execution function."""
    
    tui.display_welcome_banner()
    
    # Load the dataset
    reviews_data = load_review_data()
    
    if reviews_data is None:
        return
    
    # Confirm loading to user
    tui.display_load_confirmation(len(reviews_data))
    
    # Main program loop
    while True:
        tui.display_main_menu()
        choice = tui.get_menu_choice()
        
        if choice == 'A':
            handle_view_data_menu(reviews_data)
        elif choice == 'B':
            handle_visualisation_menu(reviews_data)
        elif choice == 'C':
            handle_export_data(reviews_data)
        elif choice == 'X':
            tui.display_exit_message()
            break
        else:
            tui.display_invalid_choice_message()

def handle_view_data_menu(reviews_data):
    """Handles the 'View Data' submenu options."""
    
    while True:
        tui.display_view_data_submenu()
        sub_choice = tui.get_menu_choice()
        
        if sub_choice == 'A':
            # Show all reviews for a specific park
            park_name = tui.get_park_name_from_user()
            park_reviews = process.filter_reviews_by_park(reviews_data, park_name)
            if park_reviews:
                tui.display_reviews_list(park_reviews, park_name)
            else:
                tui.display_no_reviews_found(park_name)
                
        elif sub_choice == 'B':
            # Count reviews by park and location
            park_name = tui.get_park_name_from_user()
            location = tui.get_location_from_user()
            count = process.count_reviews_by_park_and_location(reviews_data, park_name, location)
            tui.display_review_count_result(park_name, location, count)
            
        elif sub_choice == 'C':
            # Average rating for a park in a specific year
            park_name = tui.get_park_name_from_user()
            year = tui.get_year_from_user()
            avg_rating = process.calculate_average_rating_by_park_and_year(reviews_data, park_name, year)
            tui.display_average_rating_result(park_name, year, avg_rating)
            
        elif sub_choice == 'D':
            # Show average score per park by reviewer location
            location_averages = process.calculate_average_by_park_and_location(reviews_data)
            tui.display_location_average_report(location_averages)
            
        elif sub_choice == 'X':
            tui.display_returning_to_main()
            break
        else:
            tui.display_invalid_choice_message()

def handle_visualisation_menu(reviews_data):
    """Handles the 'Visualisations' submenu options."""
    
    while True:
        tui.display_visualisation_submenu()
        sub_choice = tui.get_menu_choice()
        
        if sub_choice == 'A':
            # Pie chart of reviews per park
            park_counts = process.count_reviews_per_park(reviews_data)
            visual.create_pie_chart(park_counts)
            
        elif sub_choice == 'B':
            # Bar chart - top 10 locations by average rating for a park
            park_name = tui.get_park_name_from_user()
            location_averages = process.calculate_average_rating_by_location(reviews_data, park_name)
            visual.create_top_locations_bar_chart(location_averages, park_name)
            
        elif sub_choice == 'C':
            # Monthly average ratings for a park
            park_name = tui.get_park_name_from_user()
            monthly_averages = process.calculate_monthly_average_ratings(reviews_data, park_name)
            visual.create_monthly_ratings_chart(monthly_averages, park_name)
            
        elif sub_choice == 'X':
            tui.display_returning_to_main()
            break
        else:
            tui.display_invalid_choice_message()

def handle_export_data(reviews_data):
    """Handles the data export functionality."""
    
    tui.display_export_format_options()
    format_choice = tui.get_menu_choice()
    
    export_formats = {'A': 'txt', 'B': 'csv', 'C': 'json'}
    
    if format_choice in export_formats:
        file_format = export_formats[format_choice]
        filename = f"disneyland_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_format}"
        
        summary_data = process.generate_park_summary(reviews_data)
        success = process.export_summary_data(summary_data, filename, file_format)
        
        if success:
            tui.display_export_success(filename)
        else:
            tui.display_export_failure()
    else:
        tui.display_invalid_choice_message()

if __name__ == "__main__":
    run()
