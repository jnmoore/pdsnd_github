import time
import pandas as pd
import datetime
import sys

CITY_DATA = {'chicago': 'chicago.csv',
            'new york city': 'new_york_city.csv',
            'washington': 'washington.csv'}

months = ['january', 'february', 'march', 'april', 'may', 'june']

#if user enters wrong value, present
invalid_option = "You did not enter a valid option. Please try again!\n"
def get_filters():
    """
    Asks user to specify a city, month, and day of the week to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or
                    "all" to apply no month filter
        (str) day - name of the day of week to filter by, or
                    "all" to apply no day filter
    """
    print("Howdy, Yall! Let's analyze some US bikeshare data!")
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    while True:
            city = input('\nWhich city would you like to begin exploring bike share data? ' +
                    'Chicago, New York City, or Washington?\n')
            if city.lower() in CITY_DATA.keys():
                print("Nice! You chose: " + city)
                break
            else:
                print(invalid_option)
                continue

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWhich month of data would you like to explore? All, January, ' +
                    'February, March, April, May, or June?\n')
        if month.lower() in ['all', 'january', 'february', 'march',
                            'april', 'may', 'june']:
            print("\nOkay, you chose: " + month)
            break
        else:
            print(invalid_option)
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nSpecify the day of data to explore. ' +
                    'All, Monday, Tuesday, Wednesday, Thursday, Friday, ' +
                    'Saturday, Sunday?\n')
        if day.lower() in ['all', 'monday', 'tuesday', 'wednesday', 'thursday',
                        'friday', 'saturday', 'sunday']:
            print("\nLastly, you chose: " + day)
            break
        else:
            print(invalid_option)
            continue
        

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month
    and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all"
                    to apply no month filter
        (str) day - name of the day of week to filter by, or "all"
                    to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    #filter by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month
    print('\nMost Common Month:')
    print(df['month'].mode()[0])

    # display the most common day of week
    print('\nMost Common Day of Week:')
    print(df['day_of_week'].mode()[0])

    # display the most common start hour
    print('\nMost Common Start Hour:')
    print(df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # display most commonly used start station
    print('\nMost Common Start Station:')
    print(df['Start Station'].mode()[0])

    # display most commonly used end station
    print('\nMost Commonly Used End Station:')
    print(df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('\nMost Frequent Start & Stop Combo')
    print(df.groupby(['Start Station', 'End Station']).size().nlargest(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # display total travel time
    print('\nTotal Travel Time:')
    print(datetime.timedelta(seconds=int(df['Trip Duration'].sum())))

    # display mean travel time
    print('\nMean Travel Time:')
    print(datetime.timedelta(seconds=int(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    print('Counts of User Types:')
    print(df['User Type'].value_counts())

    # Display counts of gender
    print('\nCounts of Gender:')
    try:
        print(df['Gender'].value_counts())
    except:
        print('Data does not include gender counts')

    # Display earliest, most recent, and most common year of birth
    print('\nEarliest, Most Recent & Most Common Date of Birth:')
    try:
        print('Earliest: {}\nMost Recent: {}\nMost Common: {}'
            .format(df['Birth Year'].min(), df['Birth Year'].max(),
                    df['Birth Year'].mode()[0]))
    except:
        print('Data does not include date of birth')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Adding to give user the option to see 5 entries at a time.
def display_data(df):
    """
    Iterate through 5 entries at a time.

    Returns:
        Print five row entries of data
    """
    #Prompt asking user if they'd like to view raw data
    question = input("\nWould you like to view raw data? Yes or No?\n ")
    if question.lower() == 'yes':
        display_more = 'yes'
    else:
        print('\nThank you for viewing. Have a nice day.\n')
        sys.exit()

    #Logic for displaying raw data
    st = 0
    while display_more == 'yes':
        df_slice = df.iloc[st: st+5]
        print(df_slice)
        st += 5   
        answer = input('\nWould you like to view 5 more data entries? Yes or No?\n')
        if answer.lower() != 'yes':
            display_more = 'no'
            break
    
def main():
    """Main body of program"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Yes or No?\n')
        if restart.lower() != 'yes':
            print('Thank you for viewing. Have a nice day.\n')
            break


if __name__ == "__main__":
    main()
