import pandas as pd
from datetime import date
import os 

def get_spi_data():

    ## Target data file
    data_file = f'.\data\soccer-spi-matches\spi_matches-{date.today()}.csv'

    ## If data doesn't exist, get it
    if not os.path.isfile(data_file):
        
        ## Read csv from url
        spi_data = pd.read_csv('https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv')

        ## Filter for Premier League matches
        spi_data = spi_data.loc[(spi_data['season'] == date.today().year) & (spi_data['league'] == 'Barclays Premier League')]

        ## Write data to csv
        spi_data.to_csv(data_file)

    ## Otherwise, open local copy
    else:
        with open(data_file) as local_file:
            spi_data = pd.read_csv(local_file)

    return spi_data