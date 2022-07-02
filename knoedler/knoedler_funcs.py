"""
Functions to help with loading/cleaning of Knoedler
and related dataset.
"""

def load_knoedler_dataset():
    """
    Returns cleaned and prepared Knoedler dataset.
    """

    path = '../data/knoedler.csv'

    df = pd.read_csv('../data/knoedler.csv')

    # Consoldate 'dollar' and 'dollars'
    df.loc[df.purch_currency == 'dollar', 'purch_currency'] = 'dollars'

    return df


def load_curr_conversion_data():
    """
    Returns cleaned and prepared Knoedler dataset merged with currency
    conversions.
    """

    # Specify path to dataset
    path = '../data/knoedler_curr_conversion.csv'

    # Load dataset
    df = pd.read_csv(path, names=['currency', 'year', 'USD-2015'])

    # Standardize values in currency col and drop dupes
    df = (
            df
            .replace({
                'Null' : np.nan,
                'US dollar [1791-2015]' : 'dollars',
                'UK pound [1658-2015]': 'pounds',
                'German mark [1871-1924]' : 'marks',
                'German reichsmark [1924-1948]': 'marks',
                'German Deutsche Mark [1948-2015]' : 'marks',
                'French franc [1795-1960]' : 'francs',
                'French franc [1960-2015]' : 'francs'
            })
            .dropna()
            .drop_duplicates(subset=['currency', 'year'])
        )

    return df


def load_knoedler_curr_conversion_dataset():
    """
    Returns an abbreviated Knoedler dataset merged with currency conversion
    set.
    """

    # Load datasets
    curr = load_curr_conversion_data()
    knoed = load_knoedler_dataset()

    # Slice out columns we want
    knoed = knoed[[
        'pi_record_no',
        'entry_date_year',
        'sale_date_year',
        'purch_amount',
        'purch_currency',
        'knoedpurch_amt',
        'knoedpurch_curr',
        'price_amount',
        'price_currency',
        'knoedshare_amt',
        'knoedshare_curr'
    ]]

    # Merge 1: Solo acquisitions
    knoed = (
        pd.merge(
            left=knoed,
            right=curr,
            how='left',
            left_on=['entry_date_year', 'purch_currency'],
            right_on=['year','currency']
        )
        .drop(columns=['year', 'currency'])
        .rename(columns={"USD-2015":"purch_conversion"})
    )

    # Merge 2: Shared acquisitions
    knoed = (
        pd.merge(
            left=knoed,
            right=curr,
            how='left',
            left_on=['entry_date_year', 'knoedpurch_curr'],
            right_on=['year','currency']
        )
        .drop(columns=['year', 'currency'])
        .rename(columns={"USD-2015":"knoedpurch_conversion"})
    )

    # Merge 3: Solo sales
    knoed = (
        pd.merge(
            left=knoed,
            right=curr,
            how='left',
            left_on=['sale_date_year', 'price_currency'],
            right_on=['year','currency']
        )
        .drop(columns=['year', 'currency'])
        .rename(columns={"USD-2015":"price_conversion"})
    )

    # Merge 4: Shared sales
    knoed = (
        pd.merge(
            left=knoed,
            right=curr,
            how='left',
            left_on=['sale_date_year', 'knoedshare_curr'],
            right_on=['year','currency']
        )
        .drop(columns=['year', 'currency'])
        .rename(columns={"USD-2015":"knoedshare_conversion"})
    )


    # Clean up inferred value columns
    cols = [
        'purch_amount',
        'knoedpurch_amt',
        'price_amount',
        'knoedshare_amt'
    ]

    chars = ['\[','\]']

    for col in cols:
        for char in chars:
            knoed[col] = (
                knoed[col].
                str.
                replace(char,'')
            )

    # Retype columns
    cols = [
        'purch_amount',
        'knoedpurch_amt',
        'price_amount',
        'knoedshare_amt',
        'purch_conversion',
        'knoedpurch_conversion',
        'price_conversion',
        'knoedshare_conversion'
    ]

    for col in cols:
        knoed[col] = pd.to_numeric(knoed[col], errors='coerce')

    # Calculate 2015 USD values
    knoed['purch_USD2015'] = knoed['purch_amount'] * knoed['purch_conversion']
    knoed['knoedpurch_USD2015'] = knoed['knoedpurch_amt'] * knoed['knoedpurch_conversion']
    knoed['price_USD2015'] = knoed['price_amount'] * knoed['price_conversion']
    knoed['knoedshare_USD2015'] = knoed['knoedshare_amt'] * knoed['knoedshare_conversion']

    return knoed
