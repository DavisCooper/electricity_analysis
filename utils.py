import numpy as np
import pandas as pd

from const import *
from pathlib import Path


DATA_DIR = Path('data')
USAGE_DATA_FN  = DATA_DIR / "TRUS_E_CUST_ICPCONS_202604_20260401_0000170112CK762.csv"
MONTHLY_USAGE_DATA_FN = DATA_DIR /  "TRUS_E_CUST_EIEP13B_202603_20260322_2054.csv"

def get_half_hourly_usage_data():
    half_hourly_data_df = pd.read_csv(USAGE_DATA_FN)
    half_hourly_data_df[START_DT_COL] = pd.to_datetime(
        half_hourly_data_df[START_DT_COL], format=DATETIME_FMT
    )
    half_hourly_data_df[END_DT_COL] = pd.to_datetime(
        half_hourly_data_df[END_DT_COL], format=DATETIME_FMT
    )
    return half_hourly_data_df

def get_monthly_usage_data():
    monthly_data_df = pd.read_csv(MONTHLY_USAGE_DATA_FN)
    monthly_data_df.rename(
        columns={
            'Read period start date and time': START_DT_COL,
            'Read period end date and time': END_DT_COL
        },
        inplace=True
    )
    monthly_data_df[START_DT_COL] = pd.to_datetime(
        monthly_data_df[START_DT_COL],
        dayfirst=True,
    )
    monthly_data_df[END_DT_COL] = pd.to_datetime(
        monthly_data_df[END_DT_COL],
        dayfirst=True, 
    )

    return monthly_data_df 




