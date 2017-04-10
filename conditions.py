#!/usr/bin/python3

import time

day_of_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def is_prime_year(year):
    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)

def get_year(days):
    year = 1970
    years = 0
    while days > 0:
        if is_prime_year(year):
            days -= 366
        else:
            days -= 365
        year += 1

    if days < 0:
        year -= 1
    return year

def get_month(days):
    year = 1970
    years = 0
    while days > 0:
        if is_prime_year(year):
            days -= 366
        else:
            days -= 365
        year += 1
    if days < 0:
        year -= 1
        
    if is_prime_year(year):
        day_of_month[2] = 29
        
    days *= -1
    print('days=',days)
    month = 12
    while days > 0:
        days -= day_of_month[month]
        month -= 1
    if days < 0:
        month += 1

    date = -days
    return month, date

seconds = int(time.time())
minutes = int(seconds / 60)
print('minutes=', minutes)
hours = int(minutes / 60)
print('hours=', hours)
days = int(hours /24)
print('days=', days)

year = get_year(days)
month,date = get_month(days)
print(year, month, date)
