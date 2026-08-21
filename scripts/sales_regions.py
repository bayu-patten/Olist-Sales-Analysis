# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 00:53:41 2026

Investigate where most sales are coming from geographically

"""
import pandas as pd
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

#%% import data
project_root = Path(__file__).resolve().parent.parent

sales_data = pd.read_csv(project_root / "data" / "processed" / "merged_data.csv")
geolocations_raw = pd.read_csv(project_root / "data" / "raw" / "olist_geolocation_dataset.csv")

#column for total price of items
sales_data["total_sale"] = sales_data["price"]*sales_data["order_item_id"]

#%% create data to be displayed
geolocations = (
    geolocations_raw
    .pivot_table(
        index="geolocation_city",
        values=["geolocation_lat", "geolocation_lng"],
        aggfunc="mean"
        )
    .reset_index()
    .rename(columns={
        "geolocation_city":"customer_city",
        "geolocation_lat":"latitude",
        "geolocation_lng":"longitude",
        })
    #.drop_duplicates("geolocation_city")
    
    )

regions = (
    sales_data
    #aggregate total sales in each city
    .pivot_table(
        index="customer_city",
        values="total_sale",
        aggfunc="sum"
        )
    .reset_index()
    .sort_values(by="total_sale", ascending=False)
    #lets add city lat/long to the data so we can place them on a map
    .merge(
        geolocations,
        on="customer_city",
        how="left"
        )
    )


world = gpd.read_file(
    "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
)

gdf = gpd.GeoDataFrame(
    regions,
    geometry=gpd.points_from_xy(
        regions["longitude"],
        regions["latitude"]),
    crs="EPSG:4326"
    )
gdf["significance"] = gdf["total_sale"] / gdf["total_sale"].max()

#%% plot data
fig, ax = plt.subplots()
world.plot(ax=ax, color="lightgrey", edgecolor="white")
gdf.plot(ax=ax, color="red", markersize=gdf["significance"]*500, alpha=0.75)
# restrict to South America
ax.set_xlim(-85, -30)
ax.set_ylim(-60, 15)
ax.set_axis_off()
plt.show()

