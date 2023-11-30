# This file contains code for suporting addressing questions in the data

"""Address a particular question that arises from the data"""

from datetime import datetime
import numpy as np
from . import assess


def get_times(df):
    times = []
    for _, row in df.iterrows():
        if type(row["date_of_transfer"]) == str:
            year = datetime.strptime(row["date_of_transfer"], "%Y-%m-%d").year
        else:
            year = row["date_of_transfer"].year
        times.append(year)
    return times


default_mapping = {'D':4.5, 'F':3.1, 'O':12, 'S':2.8, 'T':2.6}


def get_property_types(df, mapping = default_mapping):
    return [mapping[row["property_type"]] for _, row in df.iterrows()]


def get_pois(df):
    return [assess.pois(row["latitude"], row["longitude"]) for _, row in df.iterrows()]


def get_design_matrix(df):
    days = np.array(get_times(df))
    property_types = np.array(get_property_types(df))
    pois = np.array(get_pois(df))
    design = np.concatenate((days.reshape(-1, 1), property_types.reshape(-1, 1),
                            pois.reshape(-1, 1)), axis=1)
    return design


