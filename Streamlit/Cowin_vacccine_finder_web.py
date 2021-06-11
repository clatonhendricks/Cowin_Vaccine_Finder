from cowin_api import CoWinAPI
from numpy import empty
import pandas as pd
from copy import deepcopy
import datetime
import os
from requests.exceptions import HTTPError
import streamlit as st

# additional options 
no_of_days = 28   # Options 7,14,21 or 28
min_age_limit = 18  # Age limit, default 18+

BASE_DATE = datetime.datetime.now()
DATE_LIST = date_list = [BASE_DATE + datetime.timedelta(days=x * 7) for x in range(int(no_of_days / 7))]

dates = [date.strftime("%d-%m-%Y") for date in date_list]

# Start the API
cowin = CoWinAPI()

def get_availability(pincode: str, date: str, min_age_limit: int):
    """
    This function checks the availability of the Covid Vaccination and create a pandas dataframe of the available slots details.

    Parameters
    ----------
    pincode : str
        It is provided by the user 
    date : str
        Default is set 28 days
    min_age_limit : int
        Default is set 18

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
 
def findVac(pincodes):
    """
    This is the main function which uses get_availability() to check for the availability.

    """
    
    final_df = None
    try:
        for pincode in pincodes:
                for date in dates:
                        temp_df = get_availability(pincode, date, min_age_limit)
                        if final_df is not None:
                            final_df = pd.concat([final_df, temp_df])
                        else:
                            final_df = deepcopy(temp_df)
        if (final_df is not None): 
                final_df.set_index('date', inplace=True)
                st.balloons()
                st.write('Vaccine found!')
                st.write(final_df)
        else:
                st.write('No vacines found, please try another pincode(s)')
    except:
        st.error("Unable to connect to the server, if you are not in India then please use VPN to connect to India")
    # finally:
    #     st.write('No vacines found, please try another pincode(s)')

# Main Streamlit code

st.title("Cowin Vaccine Finder")
st.subheader("Please use this along with other resources to find Covid vacccine in India.")
st.markdown("**NOTE:** You can only use site if you in India or using a VPN to connect to India due to the limitation set by API released by the Indian government. ")
pincodelist = []
pincodes = st.text_input("Enter pincodes (e.g. 387001 560043)")
pincodes = pincodes.split()
if st.button("Find vaccines"):
    if pincodes == empty:
        st.write("Please enter some pincodes to search")
    else:
        with st.spinner('Searching vacinces for pincode(s)'):
            findVac(pincodes)




