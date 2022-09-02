"""
retrosheet_utils
    Contains functions to parse retrosheet datasets

    Functions
    ---------
    parse_event_file_info()
        Parses `info` record type of retrosheet event file
    
    parse_event_file_play()
        Parses `play` record type of retrosheet event file
    
    load_season_info()
        Executes parse_event_file_info() for all event files for 
        given year/season

    load_season_play()
        Executes parse_event_file_play() for all event files for
        given year/season


    Helper Functions
    ----------------
    _is_pitcher()
        Tests if current `start` pr `sub` line is a pitcher
    
    _get_pitcher()
        Returns relevant pitcher information

    _parse_id()
        Parses record with record_type == 'id'

    _parse_info()
        Parses record with record_type == 'info'

    _prepare_line()
        Prepares line for parsing

    _get_record_type()
        Returns record type

"""

import os

def parse_event_file_info(path):
    """
    Parse the `info` record type of a retrosheet event file

    Parameters
    ----------
    path : str, file path
        Retrosheet event file to be read


    Returns
    -------
    records : array of dicts
        Each dict is a game record containing `id` (unique
        game identifier) and all available `info` records 
        (number of `info` fields may vary from game to game)

    """

    # Get file contents
    file = open(path)
    lines = file.readlines()
    file.close()

    # Initialize output variables 
    record = {}               # Dict to store each `record`
    records = []              # Output list for all `record` dicts

    # Iterate through lines of retrosheet event file
    for line in lines:

        # Prepare line for parsing
        line = _prepare_line(line)
        
        # Get record type
        record_type = _get_record_type(line)

        # Parse lines of record_type `id` or `info`
        match record_type:
            case 'id':          # Start of data for a new game
                if record:
                    records.append(record)
                    record = {}
                record_label, record_value = _parse_id(line)
            
            case 'info':
                record_label, record_value = _parse_info(line)

            case _:
                continue
        
        # Add `id` or `info` key and value to `record` dict
        record[record_label] = record_value if record_value else None
    
    return records


def parse_event_file_play(path):
    """
    Parses `play` record type of a retrosheet event file

    Parameters
    ----------
    path : str, file path
        Retrosheet event file to be read

    Returns
    -------
    records : array of arrays
        Each array contains the following features:
            `id` : Unique game id
            `inning` : Inning number
            `hom_vis` : Desginates visiting team (0) or home (1)
            `player_id` : Unique player id
            `vs` : Opposing pitcher player id
            `count` : Pitch count when event occurs
            `pitches` : str, pitch sequence codes
            `event` : str, event codes
    columns : array
        Array of column names as above
    """

    # Get file contents
    file = open(path)
    lines = file.readlines()
    file.close()

    # Initialize output variables
    columns = ['id', 'inning', 'hom_vis', 'player_id', 'count', 'pitches', 'event', 'vs']
    record = []
    records = []

    # Initialize current pitcher variable
    cur_pitcher = [None, None]

    # Iterate through liens of retrosheet event file
    for line in lines:

        # Prepare line for parsing
        line = _prepare_line(line)

        # Get record type
        record_type = _get_record_type(line)

        # Parse lines of record_type `id` or `play`
        match record_type:
            case 'id':

                game_id = line[1]

            case 'start' | 'sub': # Look for starting pitchers/relievers for `vs` col

                if _is_pitcher(line):
                    team, pitcher_id = _get_pitcher(line)
                    cur_pitcher[team] = pitcher_id

            case 'play':
               
                # Build record
                record.append(game_id)
                record.extend(line[1:])
                record.append(cur_pitcher[(int(line[2]) + 1) % 2])
                
                # Append `record` to `records`
                records.append(record)

                # Re-initialize `record`
                record = []

    return records, columns


def _is_pitcher(line):
    """
    Tests if current `start` or `sub` line is a pitcher
    """
    return line[-1] == '1'


def _get_pitcher(line):
    """
    Gets relevant pitcher information
    """
    return int(line[3]), line[1]


def _parse_id(line):
    """
    Parses record with record_type == `id`
    """
    return line[0], line[1]


def _parse_info(line):
    """
    Parses record with record_type == `info`
    """
    return line[1], line[2]


def _prepare_line(line):
    """
    Prepares line for parsing

    Parameters
    ----------
    line : str

    Returns
    -------
    line : array
        Strips white space from `line` and splits on commas
    """
    return line.strip().split(',')


def _get_record_type(line):
    """
    Returns first item from input list
    """
    return line[0]


def load_season_info(year):
    """
    Runs parse_event_file_info() for all event files pertaining to a give season/year.

    Parameters
    ----------
        year : int
            Year/season we want

    Returns
    -------
        records : list of dicts
            Concatenation of `records` list returned by parse_event_file()
    """
    
    records = []

    # Get file list
    path = '../data/retrosheet/reg_season/'
    event_files = os.listdir(path)

    for event_file in event_files:
        if event_file.startswith(str(year)):
            records.extend(parse_event_file(path + event_file))

    return records


def load_season_play(year):
    """
    Runs parse_event_file_play() for all event files pertaining to a given season/year/

    Parameters
    ----------
        year : Year/season we want

    Returns
    -------
        all_records : array of arrays
            Each array contains features/columns returned by parse_event_file_play()
        columns: array
            List of columns names returned by parase_event_file_play()
    """

    all_records = []
    columns = []

    # Get file list
    path = '../data/retrosheet/reg_season/'
    event_files = os.listdir(path)

    for event_file in event_files:
        if event_file.startswith(str(year)):
            records, columns = parse_event_file_play(path + event_file)
            all_records.extend(records)

    return all_records, columns
