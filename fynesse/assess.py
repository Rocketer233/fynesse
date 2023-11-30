from typing import Dict

from .config import *
from . import access
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import osmnx as ox

"""These are the types of import we might expect in this file
import pandas
import bokeh
import seaborn
import matplotlib.pyplot as plt
import sklearn.decomposition as decomposition
import sklearn.feature_extraction"""

"""Place commands in this file to assess the data you have downloaded. How are missing values encoded, how are outliers encoded? What do columns represent, makes rure they are correctly labeled. How is the data indexed. Crete visualisation routines to assess the data (e.g. in bokeh). Ensure that date formats are correct and correctly timezoned."""


def labelled(df, latitude, longitude, box_width=0.01, box_height=0.01):
    north = latitude + box_height / 2
    south = latitude - box_height / 2
    west = longitude - box_width / 2
    east = longitude + box_width / 2
    neighbourhood = df[(df["latitude"] >= south) & (df["latitude"] <= north)
                       & (df["longitude"] >= west) & (df["longitude"] <= east)]
    return neighbourhood


# Retrieve POIs
default_tags: dict[str, bool] = {"amenity": True,
                                 "buildings": True,
                                 "historic": True,
                                 "leisure": True,
                                 "shop": True,
                                 "tourism": True}


def pois(latitude, longitude, tags=default_tags, box_width=0.02, box_height=0.02):
    # return the number of points of interests in the bounding box.
    # default bounding box size 2km
    north = latitude + box_height / 2
    south = latitude - box_height / 2
    west = longitude - box_width / 2
    east = longitude + box_width / 2
    pois = ox.features_from_bbox(north, south, east, west, tags)
    return len(pois)


def compute_avg(df, groupby, trim=None):
    # Given a dataframe, a column `groupby`, this function groups the dataframe by `groupby`
    # computes the average house prices within each group and plots the graph.
    # If trim is True, we trim outliers whose values are larger than `trim` to `trim`.
    grouping = df.groupby(groupby)['price'].mean().reset_index()
    if trim is not None:
        grouping['price'] = grouping['price'].apply(lambda x: min(x, trim))
    plt.figure(figsize=(10, 6))
    plt.bar(grouping[groupby], grouping['price'])
    plt.xlabel(groupby)
    plt.ylabel('Average Price')
    plt.title(f'Average House Prices by {groupby.capitalize()}')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.show()
