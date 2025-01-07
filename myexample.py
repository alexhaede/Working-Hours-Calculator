import streamlit as st
from myexample import calculate_end_time

from datetime import datetime, timedelta

# Constants
CONTRACTUAL_HOURS_PER_WEEK = 37.5  # Weekly work hours
WORK_DAYS_PER_WEEK = 5            # Number of workdays in a week
CONTRACT_PERCENTAGE = 0.65        # Contract percentage (65%)
EXTRA_HOURS_YEARLY = 96           # Annual extra hours
DAILY_EXTRA_MINUTES = 7           # Daily additional minutes
WORK_DAYS_PER_YEAR = 260          # Average workdays in a year

# Calculate daily hours in decimal format
daily_hours_decimal = (CONTRACTUAL_HOURS_PER_WEEK / WORK_DAYS_PER_WEEK) * CONTRACT_PERCENTAGE

# Convert decimal hours to HH:MM format
hours = int(daily_hours_decimal)
minutes = round((daily_hours_decimal - hours) * 60)

# Format the result as HH:MM
daily_hours_formatted = f"{hours}:{minutes:02d}"

# Calculate daily required work hours in decimal format
daily_required_hours = (CONTRACTUAL_HOURS_PER_WEEK / WORK_DAYS_PER_WEEK) * CONTRACT_PERCENTAGE
extra_minutes_per_day = int((EXTRA_HOURS_YEARLY * 60) / WORK_DAYS_PER_YEAR)
total_daily_minutes = (daily_required_hours * 60) + extra_minutes_per_day + DAILY_EXTRA_MINUTES

def calculate_end_time(start_time_str):
    start_time = datetime.strptime(start_time_str, "%H:%M")
    work_duration = timedelta(minutes=total_daily_minutes)
    return start_time + work_duration

def calculate_overtime_or_deficit(expected_end_time, actual_end_time_str):
    actual_end_time = datetime.strptime(actual_end_time_str, "%H:%M")
    time_difference = actual_end_time - expected_end_time
    
    # Determine if it's overtime or a deficit
    if time_difference.total_seconds() > 0:
        status = "mehr gearbeitet"
    else:
        status = "weniger gearbeitet"
    
    # Convert the time difference to hours and minutes
    time_difference_minutes = abs(int(time_difference.total_seconds() // 60))
    hours = time_difference_minutes // 60
    minutes = time_difference_minutes % 60
    
    return status, hours, minutes

def main():
    print("Arbeitszeitrechner")
    start_time_str = input("Arbeitszeitbeginn: (HH:MM, 24-Stunden Format): ")
    
    try:
        # Calculate expected end time
        expected_end_time = calculate_end_time(start_time_str)
        print(f"Um {expected_end_time.strftime('%H:%M')} ist Feierabend.")
        print(f"Arbeitszeit pro Tag: {daily_hours_formatted} Stunden.")
        print(f"96 Stunden Regel pro Tag: {extra_minutes_per_day} Minuten.")
        print(f"Vorholzeit: {DAILY_EXTRA_MINUTES} Minuten.")
        
        # Get actual end time
        actual_end_time_str = input("Feierabend tatsächlich (HH:MM, 24-Stunden Format): ")
        status, hours, minutes = calculate_overtime_or_deficit(expected_end_time, actual_end_time_str)
        
        # Display overtime or deficit
        print(f"Du hast {status}: {hours} Stunden und {minutes} Minuten.")
    except ValueError:
        print("Invalid time format. Please use HH:MM (24-hour format).")

if __name__ == "__main__":
    main()
