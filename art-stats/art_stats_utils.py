import pandas as pd
import numpy as np

def prepare_dataset(df):
    """
    A function that prepares the MoMA dataset.
    """

    # Remove records with multiple artists according to `Gender` feature
    multi_artist = df['Gender'].str.match(r'.+?\).+?\(').fillna(False)
    df = df[~ multi_artist].copy()

    # `year_acquired`: Parsed version of `DateAcquired`
    df['year_acquired'] = pd.to_datetime(df['DateAcquired']).dt.year.astype(float)

    # `date_stripped`: Cleaned version of `Date`
    df['date_stripped'] = df['Date'].str.extract(r'^.*?(\d{4} ?[-–/]? ?\d{0,4})')

    # `begun_year`: Year artwork was started, parsed from `date_stripped`
    df['begun_year'] = df['date_stripped'].str[:4].astype(float)

    # `completed_year`: Year artwork finished, parsed from `date_stripped`
    df['completed_year'] = (
        df['date_stripped'].str.extract(r'.*(\d{2})\d{2}') 
        + df['date_stripped'].str.extract(r'(\d{2})[-–/]?$')
    ).astype(float)

    # `birth_year`: Year artist born, parsed from `BeginDate`
    df['birth_year'] = df['BeginDate'].str.extract(r'\((\d+?)\)', ).astype(float)

    # Replace invaled `birth_year` with nan
    df.loc[df['birth_year'] == 0, 'birth_year'] = np.nan

    # `death_year`: Year artist died, parsed from `BeginDate`
    df['death_year'] = df['EndDate'].str.extract(r'\((\d+?)\)').astype(float)

    # `artwork_age`: Age of artwork at acquisition
    df['artwork_age'] = df['year_acquired'] - df['completed_year']

    # `living`: Encodes whether artwork was alive at time of acquisition
    df['living'] = (
        np.where((df['year_acquired'] < df['death_year']) | (df['death_year'] == 0), 1, 0)
    )

    # `artist_age`: Artist age at acquisition
    df['artist_age'] = (
        np.where(df['living'] == 1, df['year_acquired'] - df['birth_year'], np.nan)
    )

    # `years_posthumous`: Years after artist's death at acquisition
    df['years_posthumous'] = (
        np.where(df['living'] == 0, df['year_acquired'] - df['death_year'], np.nan)
    )

    # Standardize `Gender`
    gender_map = {
        '(Male)': 'Male',
        '(male)': 'Male',
        '(Female)': 'Female',
        '(female)': 'Female',
        '(Non-Binary)': 'Non-Binary',
        '(Non-binary)': 'Non-Binary'
    }
    df['Gender'] = df['Gender'].map(gender_map)
    
    return df
