import time
import pandas as pd
import numpy as np
import os
import calendar

def pick_one(name, options):
    """
    repeatedly reads string from console until it equals one of the options

    Returns:
        (str) one of the options
    """
    one = ""
    while one not in options:
        one = input("Enter the {} {}: ".format(name, options)).lower()
    return one

months = ["all", "january", "february", "march", "april", "may", "june"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city  = pick_one('city', ["chicago", "new york city", "washington"])
    month = pick_one('month', months)

    weekdays = ["all"] + list(map(str.lower, list(calendar.day_name))) 
    day   = pick_one('day', weekdays)

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
    
    if city == "chicago":
        fn = "chicago.csv"
    elif city == "new york city":
        fn = "new_york_city.csv"
    else:
        fn = "washington.csv"

    file_path = os.path.dirname(os.path.abspath(__file__)) + "\\" + fn
    df = pd.read_csv(file_path,delimiter=',')

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    month_num = months.index(month)

    if month != "all":
        df = df.loc[df['month'] == month_num]

    if day != "all":
        df = df.loc[df['day_of_week'].str.lower() == day]
    return df

def start(txt):
    print('\n{}\n'.format(txt))
    return time.time()

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    start_time = start("Calculating the Most Frequent Times of Travel...")

    # Display the most common month
    mcv_month = df['month'].mode()
    print("most common month: {}".format(months[mcv_month.tolist()[0]].capitalize()))

    # Display the most common day of week
    mcv_day_of_week = df['day_of_week'].mode() 
    print("most common day of the week: {}".format(mcv_day_of_week.tolist()[0].capitalize()))

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    mcv_hour = df['hour'].mode()
    print("most common hour: {}".format(mcv_hour.tolist()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    start_time = start("Calculating the Most Popular Stations and Trip...")

    mcv_start_station = df["Start Station"].mode()
    print("most common Start Station: {}".format(mcv_start_station.tolist()[0]))

    mcv_end_station = df["End Station"].mode()
    print("most common End Station: {}".format(mcv_end_station.tolist()[0]))

    # Display most frequent combination of start station and end station trip
    mcv_combination = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print("most common combination of Start and End Station: {}".format(mcv_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    start_time = start("Calculating Trip Duration...")

    # Display the total trips duration
    total_duration = df["Trip Duration"].sum()
    print("Total Trip Duration: {:,.0f}".format(total_duration))

    # Display the mean trip duration
    mean_duration = df["Trip Duration"].mean()
    print("Mean Trip Duration: {:.2f}".format(mean_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    start_time = start("Calculating User Stats...")

    # Display user type counts
    user_type_counts = df["User Type"].value_counts()
    print("User Type counts: {}".format(user_type_counts))

    # Some csv files hold columns Gender, birth year 
    # quit execution of this statistics if not
    if not ('Gender' in df.columns):
        print("\nThis took %s seconds." % (time.time() - start_time))
        return
    
    # Display gender counts
    gender_counts = df["Gender"].value_counts()
    print("Gender counts: {}".format(gender_counts))

    # Display birth year values
    earliest_year = int(df['Birth Year'].min())
    print("Earliest year: {}".format(earliest_year))
    most_recent_year = int(df['Birth Year'].max())
    print("Most recent year: {}".format(most_recent_year))
    most_common_year = int(df['Birth Year'].mode().iloc[0])
    print("Most common year: {}".format(most_common_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def descriptive_statistics(df, city):
    """Displays descriptive statistics on bikeshare users."""

    if df.shape[0] == 0:
        return

    chunk_size = 5
    start_index = 0
    which = "first"

    while True:
        if start_index >= df.shape[0]:
            restart = input("Do you want to restart with the first 5 rows? (yes/any other input to exit)")
            if restart.lower() == 'yes':
                which = "first"
                start_index = 0
                continue
            else:
                break

        choice = input("Do you want to check the {} 5 rows of the dataset of {}? (yes/no)".format(which, city))

        if choice.lower() == 'yes':
            chunk = df[start_index:start_index+chunk_size]
            print(chunk)
            which = "next"
            start_index += chunk_size
        elif choice.lower() == 'no':
            restart = input("Do you want to restart with the first 5 rows? (yes/any other input to exit)")
            if restart.lower() == 'yes':
                # somewhat verbose for better readability
                which = "first"
                start_index = 0
                chunk = df[start_index:start_index+chunk_size]
                print(chunk)
                which = "next"
                start_index += chunk_size
            else:
                break


def main():
    """Repeatedly as for filter critera, output statistics accordingly"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        descriptive_statistics(df, city)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
