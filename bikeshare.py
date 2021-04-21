import time
import pandas as pd
import numpy as np
import datetime as dt
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = {'CITIES': ['chicago', 'new york city', 'washington']}
    ct = pd.DataFrame(cities,index=['C','N','W'])

    while True :
        print(ct)
        city_index = input('\nPlease select the month from the CITIES (C,NYC,W) table \n')
        city_index = city_index.upper()
        if (city_index == 'C' or city_index == 'N' or city_index == 'W' ):
            city  = ct.loc[city_index].iloc[0]
            break
        else:
            print('You have entered wrong character!')

    while True :
        cq = input('You have selected "'+city+'". Do you want to continue?(y/n)')
        if cq == 'y':
            break
        elif  cq == 'n':
            quit()
        else :
            print('please enter "y" or "n"')
            continue

    # get user input for month (all, january, february, ... , june)
    months = {'MONTHS': ['all', 'January', 'February', 'March','April','May','June']}
    mt = pd.DataFrame.from_dict(months)
    while True :
        print(mt)
        try :
            month_index = int(input('\nPlease select the month from the MONTHS table (between 0-6) \n'))
        except :
            print("Only integers between 0 and 12 are allowed ")
            continue

        if month_index >= 0 and month_index <= 6 :
            break
        else:
            print("Only integers between 0 and 6 are allowed ")

    month = mt.loc[month_index].iloc[0]
    #continue or quit : cq
    while True :
        cq = input('You have selected "'+month+'". Do you want to continue?(y/n)')
        if cq == 'y':
            break
        elif  cq == 'n':
            quit()
        else :
            print('please enter "y" or "n"')



    # get user input for day of week (all, monday, tuesday, ... sunday)
    weekdays = {'DAYS': ['all', 'Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday']}
    wd = pd.DataFrame.from_dict(weekdays)
    while True :
        print(wd)
        try :
            day_index = int(input('\nPlease select the day from the DAYS table (between 0-7) \n'))
        except :
            print("Only integers between 0 and 7 are allowed \n")
            continue

        if day_index >= 0 and day_index <= 7 :
            break
        else:
            print("Only integers between 0 and 7 are allowed \n")


    day = wd.loc[day_index].iloc[0]
    while True :
        cq = input('You have selected "'+day+'". Do you want to continue?(y/n)')
        if cq == 'y':
            break
        elif  cq == 'n':
            quit()
        else :
            print('please enter "y" or "n"')



    print('-'*40)
    return city, month_index, day_index

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
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 0:

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 0:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == (day-1)]

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 0 :
        popular_month = df['month'].mode()[0]
        mf = df[df['month'] == popular_month]
        month_count = len(mf.index)
        print('Most popular month is {} with {} trips\n'.format(calendar.month_name[popular_month] ,str(month_count)))


    # display the most common day of week

    if day == 0 :
        popular_day = df['day_of_week'].mode()[0]
        wf = df[df['day_of_week'] == popular_day]
        day_count = len(wf.index)
        print('Most popular day is {} with {} trips\n'.format(calendar.day_name[popular_day] ,str(day_count)))

    # display the most common start hour

    popular_hour = df['hour'].mode()[0]
    hf = df[df['hour'] == popular_hour]
    hour_count = len(hf.index)
    print('Most popular hour  is {} with {} trips\n'.format(popular_hour ,hour_count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    # display most commonly used start station
    start_time = time.time()
    most_popular_s_station = df['Start Station'].mode()[0]
    sf = df[df['Start Station']== most_popular_s_station]
    s_station_count = len(sf.index)
    # display most commonly used end station
    most_popular_e_station = df['End Station'].mode()[0]
    ef = df[df['End Station']== most_popular_e_station]
    e_station_count = len(ef.index)
    print('Most popular start station is {} with  {} trips\nMost popular end  station is {} with  {} trips'.format(most_popular_s_station,s_station_count,most_popular_e_station,e_station_count))


    # display most frequent combination of start station and end station trip
    most_popular_trip = df.groupby(['Start Station','End Station']).size().idxmax()
    tf = df[(df['Start Station']== most_popular_trip[0])&(df['End Station']== most_popular_trip[1])]
    most_popular_trip_count = len(tf.index)
    print('The most popular trip is the between stations {} with {} trips'.format(most_popular_trip,most_popular_trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_duration = df['Trip Duration'].sum()
    trip_dration_average = df['Trip Duration'].mean()
    print('Total   Trip  Duration : {} seconds'.format(trip_duration))
    print('Average Trip  Duration : {} seconds'.format(trip_dration_average))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print('-'*20)
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The user types and total counts is: ')
    print(user_types)
    print('-'*20)


    # Display counts of gender
    #used try except if there is not gender data
    try :
        gender_type = df['Gender'].value_counts()
        print('The gender breakdown is: ')
        print(gender_type)
    except :
        print('-'*20)

    # Display earliest, most recent, and most common year of birth
    #used try except if there is not birth year data
    try :
        earliest_birth_date = int(df['Birth Year'].min())
        print('The oldest person who rent a bike is {} years old'.format(dt.datetime.now().year-earliest_birth_date))
        most_recent_birth_date = int(df['Birth Year'].max())
        print('The youngest person who rent a bike is {} years old'.format(dt.datetime.now().year-most_recent_birth_date))
        most_common_year =  int(df['Birth Year'].mode()[0])
        print('{} is the most common age who rented a bike'.format(dt.datetime.now().year-most_common_year))
    except :
        print('-'*20)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        print('\nPrinting 5 rows of the raw data')
        print('-'*40)
        #lc = loopcount
        lc = 0
        while True :
            print(df[lc:lc+5])
            opt = input('\nDo you want to see 5 more lines of raw data? Please enter "n" to stop\n')
            if opt.lower() == 'n':
                break
            lc +=5
            print('-'*40)



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
