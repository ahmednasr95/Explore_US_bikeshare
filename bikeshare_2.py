#import modules
import time
import pandas as pd
import numpy as np
import calendar
import math

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    valid_input_city = {'c': "chicago", 'ny': "new york city", 'w': "washington"}
    valid_input_month = {'jan': 'January', 'feb': 'February', 'mar': 'March', 'apr': 'April',
                         'may': 'May', 'jun': 'June', 'all': 'all'}
    valid_input_day = {'sat': 'Saturday', 'sun': 'Sunday', 'mon': 'Monday', 'tue': 'Tuesday',
                       'wed': 'Wednesday', 'thu': 'Thursday', 'fri': 'Friday', 'all': 'all'}

    print('\nHello! Let\'s explore some US bikeshare data!')
    print('Please note: \n\t-->only data for Washington D.C, Chicago, and New York City is available.')
    print('\t-->data is available for months January through June.')
    print('\t-->use all if no filter is required.')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("Please choose a city to explore its data.")
    print("Note: enter city initial(s) only.\n")
    city = input().lower()
    while city not in valid_input_city:
        print("\nLooks like you entered an invalid name. Please Try again.")
        print("Example of valid input: 'NY' for New York.\n")
        city = input().lower()

    # get user input for month (all, january, february, ... , june)
    print("\nNext, Which month would you like to view the statistics of?")
    print("Note: enter the first three letters.\n")
    month = input().lower()
    while month not in valid_input_month:
        print("\nLooks like you entered an invalid name. Please Try again.")
        print("Example of valid input: 'Jan' for January.\n")
        month = input().lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("\nFinally, Which day would you like to view the statistics of?")
    print("Note: enter the first three letters.\n")
    day = input().lower()
    while day not in valid_input_day:
        print("\nLooks like you entered an invalid name. Please Try again.")
        print("Example of valid input: 'Thu' for Thursday.\n")
        day = input().lower()

    print('-'*40)
    return valid_input_city[city], valid_input_month[month], valid_input_day[day]

def convert_date(time_series):
    """
    Converts ISO format date into day presented in the form of '0' (Monday) to '5' (Saturday).

    Args:
        (datetime64) time_series - a pandas series containing date in ISO format
    Returns:
        (list) days - a list of days
    """
    days = []
    year_series = time_series.dt.year
    month_series = time_series.dt.month
    day_series =  time_series.dt.day
    for year, month, day in zip(year_series, month_series, day_series):
        days.append(calendar.weekday(int(year), int(month), int(day)))
    return days

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
    #initializations
    month_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6}
    day_dict = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    raw_df = pd.read_csv(CITY_DATA[city])
    date_df =  pd.to_datetime(raw_df['Start Time'])
    #extract days and months
    raw_df['Days'] = convert_date(date_df)
    raw_df['Month'] = date_df.dt.month
    raw_df['Start Hours'] = date_df.dt.hour
    #in case no filter is required
    df = raw_df
    #in case month filter is required
    if 'all' not in month:
        df = raw_df[raw_df['Month'] == month_dict[month]]
    #in case day filter is required
    if 'all' not in day:
        df = df[df['Days'] == day_dict[day]]
    return df

def to_12hr_format(hours):
    """ converts the 24 hour format to 12 hour format.

        Args:
            (int) hours - hours in 24-hour format
        Returns:
            (str) new_hour - hours in 12-hour format
    """
    new_hour = 0
    if hours - 12 > 0:
        new_hour = str(hours - 12) + ' P.M'
    else:
        new_hour = str(hours) + ' A.M'
    return new_hour

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #calculate most common month, day and starting hour
    most_month = df['Month'].mode()
    most_day = df['Days'].mode()
    most_start_hour = df['Start Hours'].mode()
    month_arr = calendar.month_name
    day_arr = calendar.day_name
    # display the most common month
    print('The most common month is {}.\n'.format(month_arr[most_month[0]]))

    # display the most common day of week
    print('The most common day is {}.\n'.format(day_arr[most_day[0]]))

    # display the most common start hour
    print('The most common start hour is {}.\n'.format(to_12hr_format(most_start_hour[0])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    #calculate most common start and end stations and trip
    most_start_station = df['Start Station'].mode()
    most_end_station = df['End Station'].mode()
    df['Trip'] = df['Start Station'] +'/' + df['End Station']
    most_frequent_trip = df['Trip'].mode()[0].split('/')
    # display most commonly used start station
    print("Most commonly used starting station is {}.\n".format(most_start_station[0]))

    # display most commonly used end station
    print("Most commonly used ending station is {}.\n".format(most_end_station[0]))

    # display most frequent combination of start station and end station trip
    print("Most frequent combination of start and end stations is {} --> {}.".format(most_frequent_trip[0], most_frequent_trip[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()
    total_hours = int(total_travel_time // 3600)
    total_minutes = int((total_travel_time // 60) % 60)
    total_seconds = int(total_travel_time % 60)
    mean_hours = int(mean_travel_time // 3600)
    mean_minutes = int((mean_travel_time // 60) % 60)
    mean_seconds = int(mean_travel_time % 60)
    # display total travel time
    print("Total travel time is {} hours {} minutes {} seconds.\n".format(total_hours, total_minutes, total_seconds))

    # display mean travel time
    print("Mean travel time is {} hours {} minutes {} seconds.".format(mean_hours, mean_minutes, mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        count_user_df = df.set_index(['User Type', 'Gender']).count(level = 'User Type').filter(items = ['Trip Duration']).rename(columns = {'Trip Duration':'Count'})
        count_gender_df = df.set_index(['User Type', 'Gender']).count(level = 'Gender').filter(items = ['Trip Duration']).rename(columns = {'Trip Duration':'Count'})
        oldest_user = int(df['Birth Year'].min())
        youngest_user = int(df['Birth Year'].max())
        most_common_birth_year = df['Birth Year'].mode()

        # Display counts of user types
        print("User types:\n")
        print(count_user_df)
        print('\n')

        # Display counts of gender
        print("User genders:\n")
        print(count_gender_df)
        print('\n')

        # Display earliest, most recent, and most common year of birth
        print('Earliest year of birth: {}.\nMost recent year of birth: {}.\nMost common year of birth: {}.'.format(oldest_user, youngest_user, int(most_common_birth_year[0])))

    except KeyError:
        print('No gender or birth date data available for the selected city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        sample = input('\nWould you like to show a sample of the data?\n')
        n = 0
        #check if user wants to load some samples
        while sample.lower() == 'yes':
            try:
                print(df[n:n+5].reindex().filter(items = ['Trip Duration', 'Start Station', 'End Station', 'User Type', 'Gender']))
                n += 5
                sample = input('\nWould you like to show more data samples?\n')
            except IndexError:
                print('End of data')
                restart = input('\nWould you like to restart? Enter yes or no.\n')
                if restart.lower() != 'yes':
                    print('\n----Thanks for using our program and hope to serve you again in the future.----\n')
        #check if user wants o restart the program
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\n----Thanks for using our program and hope to serve you again in the future.----\n')
            break

if __name__ == "__main__":
	main()
