"""
Helper functions to manage water data.
"""

def add_data_point(meter=None, event=None, date=None):
    """
    Adds datapoints to the csv files storing water data and event data. If
    meter reading is given, function will write to ../data/water.csv; if event
    is given, function will write to ../data/water-events.csv; if both are given,
    function will write to both files.

    If no date is given, the function will automatically use today's date.
    """

    from datetime import datetime
    
    # Ensure we have a valid date to use
    if date: # If a date was passed, valedate it
        from dateutil import parser
        date = parser.parse(date)
        date = datetime.strftime(date, '%Y-%m-%d')
    else: # Otherwise, use today's date
        date = datetime.today().strftime('%Y-%m-%d')

    # Check for meter parameter and write to file
    if meter:
        filename = '../data/water.csv'
        f = open(filename, 'a')
        f.write("\n{0},{1}".format(date, meter))
        f.close()

    # Check for event parameter and write to file
    if event:
        filename = '../data/water-events.csv'
        f = open(filename, 'a')
        f.write("\n{0},{1}".format(date, event))
        f.close()
