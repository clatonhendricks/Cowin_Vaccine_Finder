from cowin_api import CoWinAPI
from numpy import empty
import pandas as pd
from copy import deepcopy
import datetime
import os
import logging
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--pincodes', nargs="+", help="Enter single or multiple pincodes seperated by spaces", required=True)
args = parser.parse_args()

# additional options 
no_of_days = 28   # Options 7,14,21 or 28
pincodes = args.pincodes # Get from the argument list
min_age_limit = 18  # Age limit, default 18+

BASE_DATE = datetime.datetime.now()
DATE_LIST = date_list = [BASE_DATE + datetime.timedelta(days=x * 7) for x in range(int(no_of_days / 7))]

dates = [date.strftime("%d-%m-%Y") for date in date_list]

# Start the API
cowin = CoWinAPI()

# Logging stuff
if os.path.isfile('./cowin_vaccine_finder.log'):
    os.remove('./cowin_vaccine_finder.log') # clear the old log
MY_PATH = os.getcwd()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f'{os.path.join(MY_PATH, "cowin_vaccine_finder.log")}')
fmt = logging.Formatter('%(levelname)s : %(name)s : %(asctime)s : %(message)s')
file_handler.setFormatter(fmt)
logger.addHandler(file_handler)


 
def get_availability(pincode: str, date: str, min_age_limit: int):
    """
    This function checks the availability of the Covid Vaccination and create a pandas dataframe of the available slots details.

    Parameters
    ----------
    pincode : str
        It is provided by the user in the list on line 17
    date : str
        It is auto-generated on the basis of the no. of days for which inquiry is made. Days could be 7,14,21 or 28 (preferably).
    min_age_limit : int
        It is provided by the user at line 18

    Returns
    -------
    df : Pandas dataframe
        Containing the details of the hospital where slot is available.

    """
    results = cowin.get_availability_by_pincode(pincode, date, min_age_limit)
    master_data = results['centers']
    if master_data != []:
        df = pd.DataFrame(master_data)
        if len(df):
            df = df.explode("sessions")
            df['available_capacity'] = df.sessions.apply(lambda x: x['available_capacity'])
            if df.available_capacity.sum() > 0: # check if there is availabilty 
                df['min_age_limit'] = df.sessions.apply(lambda x: x['min_age_limit'])
                df['vaccine'] = df.sessions.apply(lambda x: x['vaccine'])
                df['date'] = df.sessions.apply(lambda x: x['date'])
                df = df[["date", "available_capacity", "vaccine", "min_age_limit", "pincode", "name", "state_name", "district_name", "block_name", "fee_type"]]
                df = df[df['available_capacity'] != 0]
                df.drop_duplicates(inplace=True)
                return df

def main():
    """
    This is the main function which uses get_availability() to check for the availability.

    Parameters
    ----------
    None
    """
    if os.path.isfile('./Vaccine_Availability.txt'):
        os.remove('./Vaccine_Availability.txt')
    final_df = None
    if pincodes is None:
        print("Pincode is missing")
    else:
        for pincode in pincodes:
            for date in dates:
                temp_df = get_availability(pincode, date, min_age_limit)
                if final_df is not None:
                    final_df = pd.concat([final_df, temp_df])
                else:
                    final_df = deepcopy(temp_df)
        if (final_df is not None): # or (final_df.shape[0] != 0):
            #final_df.set_index('date', inplace=True)
            print(final_df.to_string())
            print()
            print('Vacine list is saved to VACCINE_AVAILABILITY.txt')
            final_df.to_csv(r'Vaccine_Availability.txt', sep=' ', mode='a')
            logger.info(f'Vaccines have been found and the list is saved to Vaccine_Availability.txt')
        else:
            logger.info(final_df)
            logger.info(f'There is no slot available for pincode(s) {" ".join(pincodes)}')
            print()
            print('No vacines found, please try another pincode(s)')


if __name__ == '__main__':

    main()  # comment this

    # If you want to continuosly run it in background comment the above line and uncomment the following lines and the function will be repeated after every 15 minutes

    # while True:
    #     main()
    #     time.sleep(900)
