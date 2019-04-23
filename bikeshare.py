import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def user_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter the city you would like to check:\n')
        if city.lower() == 'new york city' or city.lower() == 'chicago' or city.lower() == 'washington':
            break
        else:
            print("I didn't get that... Please try Again")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Would you like to filter by month? Ex: (january, february, ... , june) or all\n')
        months = ['january', 'february', 'march', 'april','may','june','all']
        if month.lower() in months:
            month = month.lower()
            break
        else:
            print("I didn't get that... Please try Again")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Would you like to filter by a day of the week? Ex: (mon, tue, wed, thu, fri, sat, sun) or all\n')
        days_of_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'all']
        if day.lower() in days_of_week:
            day = days_of_week.index(day.lower())
            days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
            day = days_of_week[day]
            break
        else:
            print("I didn't get that... Please try Again")

    print('-'*30)
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
    #read city csv
    df = pd.read_csv(CITY_DATA[city])

    #convert start_times to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extracting hours to new columns
    df['hour'] = df['Start Time'].dt.hour

    #extracting months and days to new columns in dataframe
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    #filtering by month if possible
    if month != 'all':
        months = ['january', 'february', 'march', 'april','may','june','all']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    #filtering by day if possible
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april','may','june']
    print("The most popular month to travel: {}".format(months[int(popular_month)-1].title()))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most popular day to travel during the week: {}".format(popular_day))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("The most popular time of day to travel is: {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*30)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most popular Starting Station: {}".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("The most popular Ending Station: {}".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['combo'] = df[['Start Station','End Station']].apply(lambda x: ' AND '.join(x),axis=1)
    print("The most frequent combination of Start Station and End Stations: {}".format(df['combo'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*30)

def timer(seconds):
    minutes = seconds // 60
    seconds = round(seconds % 60, 2)
    hours = minutes // 60
    minutes = int(minutes % 60)
    days = hours // 24
    hours = int(hours % 24)
    weeks = int(days // 7)
    days = int(days % 7)
    return weeks, days, hours, minutes, seconds

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    weeks, days, hours, minutes, seconds = timer(df['Trip Duration'].sum())
    print("The total travel time: {} weeks, {} days, {} hours, {} minutes, and {} seconds".format(weeks, days, hours, minutes, seconds))

    # display mean travel time
    weeks, days, hours, minutes, seconds = timer(df['Trip Duration'].mean())
    if weeks > 0:
        print("The average travel time: {} weeks, {} days, {} hours, {} minutes, and {} seconds".format(weeks, days, hours, minutes, seconds))
    elif days > 0:
        print("The average travel time: {} days, {} hours, {} minutes, and {} seconds".format(days, hours, minutes, seconds))
    elif hours > 0:
        print("The average travel time: {} hours, {} minutes, and {} seconds".format(hours, minutes, seconds))
    elif minutes > 0:
        print("The average travel time: {} minutes, and {} seconds".format(minutes, seconds))
    else:
        print("The average travel time: {} seconds".format(seconds))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*30)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User types:")
    print(df['User Type'].value_counts())

    # Display counts of gender
    print("\nGender Breakdown:")
    if 'Gender' in df.columns:
        df.fillna('Unknown')
        print(df['Gender'].value_counts())
    else:
        print("This city does not provide gender data")

    # Display earliest, most recent, and most common year of birth
    print("\nBirth Year Information")
    if 'Birth Year' in df.columns:
        df.fillna('Unknown')
        print("Earliest Birth Year: {}".format(int(df['Birth Year'].min())))
        print("Latest Birth Year: {}".format(int(df['Birth Year'].max())))
        print("The Most Common Birth Year: {}".format(int(df['Birth Year'].mode()[0])))
    else:
        print("This city does not provide birth year statistics")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*30)

def single_user(df):
    #single_user Information
    df = df.drop(columns=['Start Time','End Time','Trip Duration','Start Station','End Station','hour','month','day_of_week','combo'])
    df = df.fillna('Unkown')
    index = 0
    while True:
        enter = input("Hit enter to see more individual user data, to quit type anything and hit enter.")
        if enter != '':
            break
        else:
            print(df.iloc[index,:])
            index += 1

def main():
    while True:
        city, month, day = user_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        single_user(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
