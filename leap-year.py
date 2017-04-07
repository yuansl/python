#!/usr/bin/python3

import sys

def is_leap(year):
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        return True
    else:
        return False
    
week_day = { 0: 'Su', 1: 'Mo', 2: 'Tu', 3: 'We', 4: 'Th', 5: 'Fr', 6: 'Sa' }
def dayofweek(year, month, date):
    days_of_mth = [ 0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]
    base_year = 1901
    base_month = 12
    base_date = 25
    base_day = 3
    
    while base_year < year:
        tmp_date = base_date + 7
        if base_month == 2:
            if is_leap(base_year):
                days_of_mth[base_month] = 29
            else:
                days_of_mth[base_month] = 28
        base_date = tmp_date % days_of_mth[base_month]
        base_month += int(tmp_date/days_of_mth[base_month])
        if base_month > 12:
            base_year += 1
            base_month %= 12

    while base_month < month:
        tmp_date = base_date + 7
        if base_month == 2:
            if is_leap(base_year):
                days_of_mth[base_month] = 29
            else:
                days_of_mth[base_month] = 28
        base_date = tmp_date % days_of_mth[base_month]
        base_month += int(tmp_date/days_of_mth[base_month])
    return (base_day + date - base_date) % 7

def main():
    while True:
        s = input('input year month date:')
        yyyymmdd = s.split(' ')
        year = int(yyyymmdd[0])
        month = int(yyyymmdd[1])
        date = int(yyyymmdd[2])
        wday = dayofweek(year, month, date)
        print('Today is', week_day[wday])

if __name__ == '__main__':
    main()
