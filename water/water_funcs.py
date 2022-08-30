"""
Helper functions to manage water data.
"""

def add_data_point(meter=None, event=None, zone1='', zone2='', zone3='', zone4='', date=None):
    """
    Adds datapoints to the csv files storing water data, event data, and irrigation
    data.

    If meter reading is given, function will write to ../data/water.csv; if event
    is given, function will write to ../data/water-events.csv; if irrigation zone
    data are given, function will write to ../data/water-irrigation.csv. If any
    combination of these are given, function will write to all relevant files.

    If no date is given, the function will automatically use today's date.

    Parameters
    ----------
    date (str) : Date to be parsed by dateutil.parser.
        If no value passed, defaults to today's date.
    meter (float) : Meter reading
    event (str) : Description of event that might impact water usage
    zone1 (int) : Duration (minutes) of zone 1
    zone2 (int) : Duration (minutes) of zone 2
    zone3 (int) : Duration (minutes) of zone 3
    zone4 (int) : Duration (minutes) of zone 4

    Returns
    -------
    none

    """
    
    # Parse date (if provided) or return today's date
    parsed_date = _parse_date(date)

        # Check for meter parameter and write to file
    if meter:
        filename = '../data/water.csv'
        f = open(filename, 'a')
        f.write("{0},{1}".format(date, meter))
        f.close()

    # Check for event parameter and write to file
    if event:
        filename = '../data/water-events.csv'
        f = open(filename, 'a')
        f.write("{0},{1}".format(date, event))
        f.close()

    # Check for zone parameters and write to file
    if zone1 or zone2 or zone3 or zone4:
        filename = '../data/water-irrigation.csv'
        f = open(filename, 'a')
        f.write("{0},{1},{2},{3},{4}".format(date, zone1, zone2, zone3, zone4))
        f.close()

def _parse_date(date):
    """
    Helper function that returns parsed date using dateutil.parser. If 
    no value provided, function returns today's day.

    Parameters
    ----------
    date (str) : Date to parse
    
    Returns
    -------
    parsed_date (datetime.datetime) : Parsed date
    """

    from datetime import datetime
    from dateutil import parser

    if date: # If a date was passed, valedate it
        parsed_date = parser.parse(date)
        parsed_date = datetime.strftime(parsed_date, '%Y-%m-%d')
    else: # Otherwise, use today's date
        parsed_date = datetime.today().strftime('%Y-%m-%d')

    return parsed_date
