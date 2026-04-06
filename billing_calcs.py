import pandas as pd

from datetime import datetime, date, time, timedelta

def calc_simple_bill(usage_df, fixed_rate, variable_rate):
    variable_cost = usage_df.sum().sum()*variable_rate
    fixed_cost = len(usage_df)*fixed_rate
    return variable_cost + fixed_cost

def calc_electric_kiwi_bill(
        usage_df,
        off_peak_rate,
        peak_rate,
        fixed_rate,
        off_peak_1_start,
        off_peak_1_end,
        off_peak_2_start,
        off_peak_2_end, 
        hour_of_power_start,
    ):


    hour_of_power_cols = [
        hour_of_power_start,
        (
            datetime.combine(
                date.today(),
                hour_of_power_start
            )
            + timedelta(minutes=30)
        ).time(),
    ]

    off_peak_time_cols = usage_df.columns[
        (
            (usage_df.columns >= off_peak_1_start)
            & (usage_df.columns < off_peak_1_end)
        )
        | (usage_df.columns >= off_peak_2_start)
        | (usage_df.columns < off_peak_2_end)
    ]
    off_peak_time_cols = [
        time for time in off_peak_time_cols 
        if time not in hour_of_power_cols
    ]
    
    peak_time_cols = [
        time for time in usage_df.columns 
        if (
            (time not in off_peak_time_cols) 
            & (time not in hour_of_power_cols)
        ) 
    ]
    
    # Sundays have free power
    usage_df.loc[(slice(None), "Sunday"),:] = 0
    
    peak_variable_charge = usage_df[peak_time_cols].sum().sum()*peak_rate
    off_peak_variable_charge = usage_df[off_peak_time_cols].sum().sum()*off_peak_rate
    fixed_cost = len(usage_df)*fixed_rate

    return peak_variable_charge + off_peak_variable_charge + fixed_cost

def calc_contact_low_user_bill(usage_df):

    free_charge_period_start = time(9,00)
    free_charge_period_end = time(17,00)
    free_days = slice("Saturday", "Sunday")
    fixed_rate = 1.725
    variable_rate = 0.3381

    free_cols = usage_df.columns[
        (
            (usage_df.columns >= free_charge_period_start)
            & (usage_df.columns < free_charge_period_end)
        )
    ]

    usage_df.loc[(slice(None), free_days), free_cols] = 0

    return calc_simple_bill(usage_df, fixed_rate, variable_rate)

def calc_contact_good_charge_bill(usage_df):

    reduced_billing_start = time(21,00)
    reduced_billing_end = time(7,00)
    fixed_rate = 1.725
    variable_rate = 0.3726

    reduced_billing_cols = usage_df.columns[
        (usage_df.columns >= reduced_billing_start)
        | (usage_df.columns < reduced_billing_end)
    ]

    usage_df[reduced_billing_cols] = usage_df[reduced_billing_cols]/2

    return calc_simple_bill(usage_df, fixed_rate, variable_rate)



