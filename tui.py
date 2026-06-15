"""
Text User Interface module - handles all console-based input and output operations.

This module is responsible for displaying information to users and collecting
their responses. No data processing or analysis happens here.
"""

def display_welcome_banner():  
    """Shows the program title and introductory information."""
    print("\n" + "=" * 60)
    print("    D I S N E Y L A N D   R E V I E W   A N A L Y S E R")
    print("=" * 60)
    print("\nWelcome! This tool helps you explore and analyse thousands")
    print("of Disneyland park reviews from around the world.\n")

def display_load_confirmation(row_count):
    """Confirms successful data loading with row count."""
    print(f"\n[SUCCESS] Dataset loaded successfully!")
    print(f"[INFO] Total reviews in dataset: {row_count}\n")

def display_main_menu():
    """Displays the main menu options."""
    print("\n" + "-" * 40)
    print("M A I N   M E N U")
    print("-" * 40)
    print("[A] View Data & Reports")
    print("[B] Generate Visualisations")
    print("[C] Export Summary Data")
    print("[X] Exit Program")
    print("-" * 40)

def display_view_data_submenu():
    """Displays the view data submenu options."""
    print("\n" + "-" * 40)
    print("V I E W   D A T A   M E N U")
    print("-" * 40)
    print("[A] Show all reviews for a specific park")
    print("[B] Count reviews by park and location")
    print("[C] Average rating for a park in a specific year")
    print("[D] Average score per park by reviewer location")
    print("[X] Return to main menu")
    print("-" * 40)

def display_visualisation_submenu():
    """Displays the visualisation submenu options."""
    print("\n" + "-" * 40)
    print("V I S U A L I S A T I O N   M E N U")
    print("-" * 40)
    print("[A] Pie chart - Reviews per park")
    print("[B] Bar chart - Top 10 locations by average rating")
    print("[C] Bar chart - Monthly average ratings for a park")
    print("[X] Return to main menu")
    print("-" * 40)

def display_export_format_options():
    """Displays export format options."""
    print("\n" + "-" * 40)
    print("E X P O R T   F O R M A T")
    print("-" * 40)
    print("[A] TXT (plain text report)")
    print("[B] CSV (spreadsheet compatible)")
    print("[C] JSON (structured data format)")
    print("-" * 40)
    print("Which format would you like to use?")

def get_menu_choice():
    """
    Gets a menu selection from the user.
    
    Returns:
        str: The user's selected option (uppercase)
    """
    choice = input("\nEnter your selection: ").strip().upper()
    print(f"\nYou selected: {choice}")
    return choice

def get_park_name_from_user():
    """
    Asks the user which park they want to analyse.
    
    Returns:
        str: The park name entered by the user
    """
    print("\nWhich Disneyland park would you like to analyse?")
    print("(Options: Disneyland_California, Disneyland_Paris, Disneyland_HongKong, Disneyland_Shanghai)")
    park = input("Park name: ").strip()
    return park

def get_location_from_user():
    """
    Asks the user for a reviewer location.
    
    Returns:
        str: The location entered by the user
    """
    location = input("Enter reviewer's location (e.g., United Kingdom, USA, Brazil): ").strip()
    return location

def get_year_from_user():
    """
    Asks the user for a year to filter reviews.
    
    Returns:
        int: The year entered by the user
    """
    while True:
        try:
            year = int(input("Enter year (e.g., 2018, 2019, 2020): ").strip())
            return year
        except ValueError:
            print("Please enter a valid year (numbers only).")

def display_reviews_list(reviews, park_name):
    """
    Displays all reviews for a specific park.
    
    Args:
        reviews (list): List of review dictionaries
        park_name (str): Name of the park
    """
    print(f"\n{'=' * 50}")
    print(f"REVIEWS FOR {park_name.upper()}")
    print(f"{'=' * 50}")
    print(f"Total reviews found: {len(reviews)}\n")
    
    for idx, review in enumerate(reviews[:20], 1):  # Show first 20 to avoid clutter
        print(f"{idx}. Rating: {review['rating']}/5 | Date: {review['year_month']} | From: {review['reviewer_location']}")
    
    if len(reviews) > 20:
        print(f"\n... and {len(reviews) - 20} more reviews.")
    
    input("\nPress Enter to continue...")

def display_review_count_result(park_name, location, count):
    """
    Displays the count of reviews matching specific criteria.
    """
    print(f"\n[RESULT] {park_name} has received {count} review(s) from {location}.")
    input("\nPress Enter to continue...")

def display_average_rating_result(park_name, year, average):
    """
    Displays the average rating calculation result.
    """
    if average == 0:
        print(f"\n[RESULT] No reviews found for {park_name} in {year}.")
    else:
        print(f"\n[RESULT] Average rating for {park_name} in {year}: {average}/5.0")
    input("\nPress Enter to continue...")

def display_no_reviews_found(park_name):
    """Informs user that no reviews exist for the specified park."""
    print(f"\n[WARNING] No reviews found for '{park_name}'. Please check the park name and try again.")
    input("\nPress Enter to continue...")

def display_location_average_report(location_averages):
    """
    Displays the complete report of average ratings by park and location.
    """
    print("\n" + "=" * 60)
    print("AVERAGE RATING PER PARK BY REVIEWER LOCATION")
    print("=" * 60)
    
    for park, locations in location_averages.items():
        print(f"\n{park}:")
        print("-" * 30)
        for location, avg in sorted(locations.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {location}: {avg}/5.0")
        if len(locations) > 10:
            print(f"  ... and {len(locations) - 10} more locations.")
    
    input("\nPress Enter to continue...")

def display_error_message(message):
    """Displays an error message to the user."""
    print(f"\n[ERROR] {message}")

def display_invalid_choice_message():
    """Informs user they made an invalid menu selection."""
    print("\n[ERROR] Invalid selection! Please choose from the available options (A, B, C, or X).")
    input("\nPress Enter to continue...")

def display_exit_message():
    """Displays goodbye message when program ends."""
    print("\n" + "=" * 60)
    print("Thank you for using the Disneyland Review Analyser!")
    print("Goodbye!")
    print("=" * 60 + "\n")

def display_returning_to_main():
    """Confirms return to main menu."""
    print("\n[INFO] Returning to main menu...")

def display_export_success(filename):
    """Confirms successful data export."""
    print(f"\n[SUCCESS] Data exported successfully!")
    print(f"[INFO] File saved as: {filename}")
    input("\nPress Enter to continue...")

def display_export_failure():
    """Informs user that export failed."""
    print("\n[ERROR] Failed to export data. Please check your disk space and permissions.")
    input("\nPress Enter to continue...")
