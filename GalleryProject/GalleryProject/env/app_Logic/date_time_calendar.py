from datetime import datetime
import calendar
get_now = datetime.now()




# ---------------------------------------------------------------------------------------------------------------- #
# defualt month and year, defaults to todays date
# ---------------------------------------------------------------------------------------------------------------- #

todays_date = datetime.now()
month = todays_date.strftime("%B")
year_number = int(todays_date.strftime("%Y"))
month = month.title()
month_number = list(calendar.month_name).index(month)
month_number = int(month_number)

def date_passed_check(check_date):
    this_date = datetime.date(todays_date)
    date_passed = ''
    if this_date >= check_date:
        date_passed = True
    else:
        date_passed = False
        
    return date_passed

# ---------------------------------------------------------------------------------------------------------------- #
# Calendar Function
# ---------------------------------------------------------------------------------------------------------------- #

def cal_gen(month_set=month_number, year_set=year_number):
    
    
    
    # --------------#
    # List and dictionaries
    # --------------#

    months_length = {
        1: int(calendar.monthrange(year_set, 1)[1]),
        2: int(calendar.monthrange(year_set, 2)[1]),
        3: int(calendar.monthrange(year_set, 3)[1]),
        4: int(calendar.monthrange(year_set, 4)[1]),
        5: int(calendar.monthrange(year_set, 5)[1]),
        6: int(calendar.monthrange(year_set, 6)[1]),
        7: int(calendar.monthrange(year_set, 7)[1]),
        8: int(calendar.monthrange(year_set, 8)[1]),
        9: int(calendar.monthrange(year_set, 9)[1]),
        10: int(calendar.monthrange(year_set, 10)[1]),
        11: int(calendar.monthrange(year_set, 11)[1]),
        12: int(calendar.monthrange(year_set, 12)[1]),
    }

    dotw = {
        'Mon': 1,
        'Tue': 2,
        'Wed': 3,
        'Thu': 4,
        'Fri': 5,
        'Sat': 6,
        'Sun': 7
    }
    
    # create balnk list

    list_42days = []
    week1 = {}
    week2 = {}
    week3 = {}
    week4 = {}
    week5 = {}
    week6 = {}
    week_number = 1
    last_month_name = ''
    next_month_name = ''

    last_day = months_length.get(month_set)
    
    # lamnda function to get the last and next month
    previous_month = lambda month_set: 12 if month_set == 1 else month_set - 1
    next_month = lambda month_set: 1 if month_set == 12 else month_set + 1

    # creats an object for the current calendar month, with all the dates
    calendar_month = datetime(year_set, month_set, 1)

    # gets the first day of the week name
    first_day_name = calendar_month.strftime('%a')
    # converts the frist day into a number of the week, minus two to adjust monday as the first day in the week
    frist_cal_day = dotw.get(first_day_name) - 2

    start_current_month_count = frist_cal_day + 1
    end_current_month_count = frist_cal_day + last_day + 1

    # determins the final length of numbers, using 42 as the number of days in the calendar
    tail_end = 42 - (frist_cal_day + last_day + 1)
    


    previous_lastday = months_length.get(previous_month(month_set))


    # first date in 42 days, useing the first day, current cal week number minus the last day of the previus month
    frist_cal_date = int(previous_lastday) - frist_cal_day

    print(previous_lastday)
    # append days in order for the list of 42 days
    for last_month_days in range(frist_cal_date, previous_lastday + 1):
        list_42days.append(last_month_days)

    for selected_days in range(1, last_day + 1):
        list_42days.append(selected_days)

    for next_month_days in range(1, tail_end + 1):
        list_42days.append(next_month_days)
    if len(list_42days) > 42:
        print('error', len(list_42days), list_42days)

    # ---------------------------------------------------------------------------------------------------------------- #
    # three sets of loops to create the dict of weeks for the calendar
    # ---------------------------------------------------------------------------------------------------------------- #

    # for the start of the next month count
    if list_42days[0] > 15:
        for days in list_42days[0:start_current_month_count]:
            if previous_month(month_set) == 12:
                day_name_checker = datetime((year_set - 1), previous_month(month_set), days)
            if previous_month(month_set) != 12:
                day_name_checker = datetime(year_set, previous_month(month_set), days)

            last_month_name = day_name_checker.strftime('%B')
            day_name_last = day_name_checker.strftime('%a')

            # Append the dictionary for week number and day_name and day number
            if week_number == 1:
                days_compact = {'day': days, 'date': day_name_checker}
                week1[day_name_last] = days_compact
            if week_number == 2:
                days_compact = {'day': days, 'date': day_name_checker}
                week2[day_name_last] = days_compact

            # Check if it's Sunday and if so bumpbs it up the week counter
            if day_name_last == 'Sun':

                week_number += 1
    else:
        if previous_month(month_set) == 12:
            day_name_checker = datetime((year_set - 1), previous_month(month_set), 1)
        if previous_month(month_set) != 12:
            day_name_checker = datetime(year_set, previous_month(month_set), 1)

        last_month_name = day_name_checker.strftime('%B')

    # for the main calendar

    for days in list_42days[start_current_month_count:end_current_month_count ]:
        day_name_checker = datetime(year_set, month_set, days)
        day_name = day_name_checker.strftime('%a')
        month_name = day_name_checker.strftime('%B')

        # Append the dictionary for week number and day_name and day number
        if week_number == 1:
            days_compact = {'day': days, 'date': day_name_checker}
            week1[day_name] = days_compact
        if week_number == 2:
            days_compact = {'day': days, 'date': day_name_checker}
            week2[day_name] = days_compact
        if week_number == 3:
            days_compact = {'day': days, 'date': day_name_checker}
            week3[day_name] = days_compact
        if week_number == 4:
            days_compact = {'day': days, 'date': day_name_checker}
            week4[day_name] = days_compact
        if week_number == 5:
            days_compact = {'day': days, 'date': day_name_checker}
            week5[day_name] = days_compact
        if week_number == 6:
            days_compact = {'day': days, 'date': day_name_checker}
            week6[day_name] = days_compact

        # Check if it's Sunday and if so bumpbs it up the week counter
        if day_name == 'Sun':

            week_number += 1

    if list_42days[-1] < 15:
        for days in list_42days[end_current_month_count:]:
            if next_month(month_set) == 1:
                day_name_checker = datetime((year_set + 1), next_month(month_set), days)
            else:
                day_name_checker = datetime(year_set, next_month(month_set), days)

            next_month_name = day_name_checker.strftime('%B')
            day_name_next = day_name_checker.strftime('%a')


            # Append the dictionary for week number and day_name and day number

            if week_number == 5:
                days_compact = {'day': days, 'date': day_name_checker}
                week5[day_name_next] = days_compact
            if week_number == 6:
                days_compact = {'day': days, 'date': day_name_checker}
                week6[day_name_next] = days_compact

            # Check if it's Sunday and if so bumpbs it up the week counter
            if day_name_next == 'Sun':

                week_number += 1
    else:
        if next_month(month_set) == 1:
            day_name_checker = datetime((year_set + 1), next_month(month_set), 1)
        else:
            day_name_checker = datetime(year_set, next_month(month_set), 1)

        next_month_name = day_name_checker.strftime('%B')

    cal_date = datetime(year_set, month_set, 1)
    # Append the dictionary for the month with the list of week dict, that has each day of the week
    month_dates = {'week1':week1, 'week2': week2, 'week3': week3, 'week4': week4, 'week5':week5, 'week6': week6}
    return last_month_name, month_name, next_month_name, month_dates, year_number, todays_date, cal_date

#day = get_now.strftime("%d")
month = get_now.strftime("%m")
year = get_now.strftime("%Y")
year = int(year)
month = int(month)


#month0, month1, month2, cal = last_days(5, year)





#month0, month1, month2, cal, year_new, todays_date = cal_gen()
#print(month0, month1, month2)

