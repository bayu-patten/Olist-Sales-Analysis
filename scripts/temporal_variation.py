# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 20:50:30 2026

Investigate variation in product type sold over time and seasonally
See variation in count of items sold and in $ value

@author: imbkp20
"""
#%%
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

project_root = Path(__file__).resolve().parent.parent

sales_data = pd.read_csv(project_root / "data" / "processed" / "merged_data.csv")
#%% construct data to be used for plots
#we only want to deal with data regarding completed orders
sales_data = sales_data[sales_data["order_status"] == "delivered"]
sales_data = sales_data[sales_data["order_delivered_customer_date"].notna()]

sales_data["total_sale"] = sales_data["price"]*sales_data["order_item_id"]
sales_data["sale_month"] = sales_data["order_delivered_customer_date"].dt.to_period('M')

plot_data = sales_data.pivot_table(
    index=["sale_month", "product_category_name_english"],
    values=["order_item_id", "total_sale"]
    ).reset_index()
#%%
fig, ax = plt.subplots()

for category, group in plot_data.groupby("product_category_name_english"):
    plt.plot(
        group["sale_month"],
        group["total_sale"],
        label=category
    )

plt.legend()
plt.savefig(project_root / "timeseries_sales.png")
plt.show()