"""
retrosheet_utils
    Contains functions to parse retrosheet datasets
"""

import os

def parse_event_file_info(f):
    """
    Parse the `info` record type of a retrosheet event file

    Parameters
    ----------
    f : str, file path
        Retrosheet event file to be read


    Returns
    -------
    records : array of dicts
        Each dict is a game record containing `id` (unique
        game identifier) and all available `info` records 
        (number of `info` fields may vary from game to game)

    """

    file = open(f)
    lines = file.readlines()
    file.close()

    record = {}               # initialize dict to store each `record`
    records = []              # output list for each `record`

    # Iterate through lines of retrosheet event file
    for line in lines:

        # Prepare line for parsing
        line = line.strip().split(',')

        # Parse line
#        record_type, record_labels, record_values = _parse_line()

        record_type = line[0]   # We want lines whose first element is `id` or `info`

        # Parse 'id' record type
        if record_type == 'id': # Start of data for a new game

            # Before building new game `record`, append previous game `record` to `records`
            if record:
                records.append(record)
                record = {}
            
            record_label = line[0]
            record_value = line[1]
        
        
        # Parse 'info' record type
        elif record_type == 'info':

            record_label = line[1]        # `info` category, i.e., `starttime`
            record_value = line[2]        # value accomanyying `info` category

        
        # Add `id` or `info` key and value to `record` dict
        record[record_label] = record_value if record_value else None
    
    return records


def _parse_line(line):
    """
    Helper function that parses line type

    Parameters
    ----------
    line : array

    Returns
    -------
    record_type : str
        options:
            `id`
            `version`
            `info`
            `start`
            `sub`
            `play`
            `badj`
            `padj`
            `ladj`
            `radj`
            `data`
            `com`
    record_labels : array (n,)
        column names
    record_values : array (n,)
        row of values
    """
    
    record_type = line[0]
    
    match record_type:
        case 'id':
            return None, None, None
        case 'version':
            return None, None, None
        case 'info':
            return None, None, None
        case 'start':
            return None, None, None
        case 'sub':
            return None, None, None
        case 'play':
            return None, None, None
        case 'badj':
            return None, None, None
        case 'padj':
            return None, None, None
        case 'ladj':
            return None, None, None
        case 'radj':
            return None, None, None
        case 'data':
            return None, None, None
        case 'com':
            return None, None, None


def load_season_info(year):
    """
    Runs parse_event_file_info for all event files pertaining to a give season/year.

    Parameters
    ----------
        year : int
            Year/season we want

    Returns
    -------
        records : list of dicts
            Concatenation of `records` list returned by parse_event_file_info()
    """
    
    records = []

    # Get file list
    path = '../data/retrosheet/reg_season/'
    event_files = os.listdir(path)

    for event_file in event_files:
        if event_file.startswith(str(year)):
            records.extend(parse_event_file_info(path + event_file))

    return records




if __name__ == '__main__':
    
    records = parse_info('../data/retrosheet/reg_season/2017LAN.EVN')
    for record in records:
        print(record)
