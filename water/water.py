"""
Helper functions to manage water data.
"""

def add_data_point(meter, filename='../data/water.csv', date=None):
    """
    Adds a meter reading to the csv file storing water data
    If no date is given, the function will automatically use today's date.
    If no filename is given, the function will default to water.csv.
    """

    from datetime import datetime
    
    # Ensure we have a valid date to use
    if date: # If a date was passed, valedate it
        from dateutil import parser
        date = parser.parse(date)
        date = datetime.strftime(date, '%Y-%m-%d')
    else: # Otherwise, use today's date
        date = datetime.today().strftime('%Y-%m-%d')

    # Open csv file in append mode and write to it
    f = open(filename, 'a')
    f.write("\n{0},{1}".format(date, meter))
    f.close()
