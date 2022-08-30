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
    
    parsed_date = _parse_date(date)
    
    if meter:
        _update_meter(parsed_date, meter, path='../data/water.csv')
    if event:
        _update_events(parsed_date, event, path='../data/water-events.csv')
    if zone1 or zone2 or zone3 or zone4:
        _update_zones(parsed_date, zone1, zone2, zone3, zone4, path='../data/water-irrigation.csv')

    return


def _update_meter(parsed_date, meter, path):
    """
    Appends `parsed_date` and `meter` to data file at `path`

    """
    
    f = open(path, 'a')
    f.write("{0},{1}".format(parsed_date, meter))
    f.close()

    return


def _update_events(parsed_date, event, path):
    """
    Appends `parsed_date` and `meter` to data file at `path`
    """

    f = open(path, 'a')
    f.write("{0},{1}".format(parsed_date, event))
    f.close()
    
    return


def _update_zones(parsed_date, zone1, zone2, zone3, zone4, path):
    """
    Appends `parsed_date`, `zone1`, `zone2`, `zone3`, and `zone4` to file at
    path.
    """

    f = open(path, 'a')
    f.write("{0},{1},{2},{3},{4}".format(parsed_date, zone1, zone2, zone3, zone4))
    f.close()

    return


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
