from datetime import timedelta, datetime

# Swedish public holidays (without year)
swedish_holidays = [
    '01-01', '01-06', '04-07', '04-09', '04-10',
    '05-01', '05-18', '06-06', '06-24', '11-04',
    '12-25', '12-26'
    # Add more holidays here if needed...
]

def is_valid_defence_date(defence_date):
    month_day = (defence_date.month, defence_date.day)
    return not (6, 16) <= month_day <= (8, 14)

def adjust_for_holidays_and_weekends(date):
    current_year = date.year
    holidays_for_current_year = [f"{current_year}-{holiday}" for holiday in swedish_holidays]
    while date.strftime('%Y-%m-%d') in holidays_for_current_year or date.weekday() >= 5:
        date += timedelta(days=1)
    return date


def calculate_key_dates_slu(defence_date_str):
    defence_date = datetime.strptime(defence_date_str, '%Y-%m-%d').date()
    defence_date = adjust_for_holidays_and_weekends(defence_date)  # Adjusting the defence date as well
    if not is_valid_defence_date(defence_date):
        return {"error": "Defences are not held between June 16 and August 14. Please enter a valid date."}

    # Calculate and adjust key dates
    six_months_before = adjust_for_holidays_and_weekends(defence_date - timedelta(days=180))
    three_months_before = adjust_for_holidays_and_weekends(defence_date - timedelta(days=90))
    four_weeks_before_nailing = adjust_for_holidays_and_weekends(defence_date - timedelta(days=49))
    three_weeks_before = adjust_for_holidays_and_weekends(defence_date - timedelta(days=21))
    
    return {
        'defence_date': defence_date,
        'six_months_before': six_months_before,
        'three_months_before': three_months_before,
        'four_weeks_before_nailing': four_weeks_before_nailing,
        'three_weeks_before': three_weeks_before
    }

def calculate_key_dates_uppsala(defence_date_str):
    defence_date = datetime.strptime(defence_date_str, '%Y-%m-%d').date()
    defence_date = adjust_for_holidays_and_weekends(defence_date)
    if not is_valid_defence_date(defence_date):
        return {"error": "Defences are not held between June 16 and August 14. Please enter a valid date."}

    # Calculate and adjust key dates
    five_months_before = adjust_for_holidays_and_weekends(defence_date - timedelta(days=150))
    fourteen_weeks_before = adjust_for_holidays_and_weekends(defence_date - timedelta(weeks=14))
    twelve_weeks_before = adjust_for_holidays_and_weekends(defence_date - timedelta(weeks=12))
    seven_weeks_before = adjust_for_holidays_and_weekends(defence_date - timedelta(weeks=7))
    three_weeks_before = adjust_for_holidays_and_weekends(defence_date - timedelta(weeks=3))

    return {
        'defence_date': defence_date,
        'five_months_before': five_months_before,
        'fourteen_weeks_before': fourteen_weeks_before,
        'twelve_weeks_before': twelve_weeks_before,
        'seven_weeks_before': seven_weeks_before,
        'three_weeks_before': three_weeks_before
    }