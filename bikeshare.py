# -*- coding: utf-8 -*-
"""
Udacity - Programming for Data Science - Project 2

This project utilitizes sanitized data from bikeshare programs in Chicago, New
York City, and Washington.  Additional data sources may be added as available.

@author: annagoben
"""

import time
import calendar
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


month_dict = {'all':0, 
              'january':1, 
              'february':2, 
              'march':3, 
              'april':4, 
              'may':5, 
              'june':6}


day_dict = {'all': 9, 
            'monday': 1, 
            'tuesday': 2, 
            'wednesday': 3, 
            'thursday': 4, 
            'friday': 5, 
            'saturday': 6, 
            'sunday': 7}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Please choose a city: Chicago, New York City, or Washington:\n').lower()
            if city in CITY_DATA:
                break
            else:
                print('Invalid entry.  Please your selection enter from the supplied list.')
        except:
            print('Invalid entry.  Please your selection enter from the supplied list.')
        finally: 
            print('You entered:', city.title())

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Please choose a month (January-June) by name to evaluate (enter "all" for full data):\n').lower()
            if month in month_dict:
                break
            else:
                print('Entry value not recognized.  Please enter your selection again.')
        except:
            print('Entry value not recognized.  Please enter your selection again.')
        finally: 
            print('You entered:', month.title())

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Please choose a day of the week to evaluate  (enter "all" for full weekly data):\n').lower()
            if day in day_dict:
                break
            else:
                print('Invalid entry.  Please enter your selection again.')
        except:
            print('Invalid entry.  Please enter your selection again.')
        finally: 
            print('You entered:', day.title())

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['trip'] = (df['Start Station'] + ' to ' + df['End Station'])
    
    if month != 'all':
        month = month_dict[month]
        # filter by month if applicable
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]    

    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    print('Statistics for ', city.title())
    if month == 'all':
        month_name = 'any month'
    else:
        month_name = month.title()
    if day == 'all':
        day_name = 'any day'
    else:
        day_name = day.title() + 's'
    # Displays the most common month if no month is selected as a filter
    if month == 'all':
        most_common_month = df['month'].mode()[0]
        most_common_month = calendar.month_name[most_common_month]
    
        print('Most popular month of the year:', most_common_month)

    # Displays the most common day of week for selected month if no day filter
    if day == 'all':
        most_common_day = df['day_of_week'].mode()[0]
        
        print('Most popular day of the week in', month_name, ': ', most_common_day)

    # Calculate and display the most common start hour by selected day/month
    df['hour'] = df['Start Time'].dt.hour

    # Calculate and display the most common hour (from 0 to 23)
    most_common_hour = df['hour'].mode()[0]
    if most_common_hour < 12:
        most_common_hour = str(most_common_hour) + " AM"
    else:
        most_common_hour = str(most_common_hour-12) + " PM"
    print('Most popular hour on', day_name, 'in', month_name, ': ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Calculate and display most commonly used start station
    most_common_start_stn = df['Start Station'].mode()[0]

    print('Most common starting station:', most_common_start_stn)
    # Calculate and display most commonly used end station
    most_common_end_stn = df['End Station'].mode()[0]
    
    print('Most common ending station:', most_common_end_stn)

    # Calculate and display most frequent combination of start station and end station trip
    most_common_trip = df['trip'].mode()[0]
    
    print('Most common trip:', most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    def sec_time(time_in_sec):
        """Creates printable string that breaks a group of seconds
           into hours, minutes, and remaining seconds 
        """
        hours = (str('{:,}'.format(int(time_in_sec / 3600))))
        mins = (str(int((time_in_sec / 60) % 60)))
        secs = (str(int(time_in_sec % 60)))
        if hours == '0':
            time = (mins + ' minutes, and ' + secs + ' seconds')
        else:
            time = (hours + ' hours, ' + mins + ' minutes, and ' + secs + ' seconds')
        return (time)
        
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate and display total travel time
    total_travel = df['Trip Duration'].sum()
    # Convert total seconds to larger units
    travel_time = (sec_time(total_travel))
    print('Total travel time for selected dates :', travel_time)

    # Calculate and display mean travel time
    average_travel = df['Trip Duration'].mean()
    # Convert mean seconds to larger units
    avg_travel = (sec_time(average_travel))
    print('Average trip time for selected dates :', avg_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Calculate and display counts of user types
    user_types = df['User Type'].value_counts()
    
    print('Participant types for the selected dates: \n')
    print(user_types)

    # Calculate and display counts of gender
    if city == 'washington':
        print('\nNo gender information available.\n')
    else:
        gender = df['Gender'].fillna('No data').value_counts()
        print('\nParticipants by gender for the selected dates:\n')
        print(gender)

    # Calculate and display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('\nNo birth year information available.\n')
    else:
        birth_year = df['Birth Year'].dropna(axis = 0)
        earliest_year = int(birth_year.min())
        most_recent_year = int(birth_year.max())
        most_common_year = int(birth_year.mode()[0])
        print('\nThe earliest reported year of birth is:', earliest_year)
        print('\nThe most recent reported year of birth is:', most_recent_year)
        print('\nThe most commonly reported year of birth is:', most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def review_data(df):
    """ This iterates and prints through the available raw data 5 lines at a time. """
    # Initialize iloc variables
    start = 0
    stop = 5
    # Print initial data set
    print(df.iloc[start:stop])
    while True:
        cont = input('Do you wish to continue? Y/N\n').lower()
        if cont == 'y':
            start += 5
            stop += 5
            print(df.iloc[start:stop])
            df.head()
        elif cont == 'n':
            break
        else:
            print('Invalid entry.  Please enter your selection again.')
        

def main():
    while True:
        # Get inputs from user and data sources
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # Process and print statistics
        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        
        # Offer raw data
        offer_data = 'y'
        while offer_data == 'y':
            offer_data = input('\nWould you like to review the full data? Y/N\n').lower()
            if offer_data == 'y':
                review_data(df)
                offer_data = 'n'
            elif offer_data == 'n':
                break
            else:
                print('Invalid entry.  Please enter your selection again.')
        
        # Offer restart options
        restart = input('\nWould you like to restart? Enter yes to continue or any other value to quit.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

    
