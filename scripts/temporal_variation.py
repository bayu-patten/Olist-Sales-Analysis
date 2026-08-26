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

project_root = Path(__file__).resolve().parent.parent

sales_data = pd.read_csv(project_root / "data" / "processed" / "merged_data.csv")
#%% construct data to be used for plots
#we only want to deal with data regarding completed orders
sales_data = sales_data[sales_data["order_status"] == "delivered"]
sales_data = sales_data[sales_data["order_delivered_customer_date"].notna()]

sales_data["total_sale"] = sales_data["price"]*sales_data["order_item_id"]
sales_data["sale_month"] = (
    pd.to_datetime(sales_data["order_delivered_customer_date"])
    .dt.to_period('M')
    .dt.to_timestamp()
    )
#filter to months with consistent complete data (before feb 2017 has far too
#few orders and after aug 2018 is also suspiciously low)
sales_data = sales_data[sales_data["sale_month"].between(
    left="2017-02-01",
    right="2018-08-01",
    inclusive="both"
    )]

#there are far too many categories of product to plot all of them.
#we should limit to the top N categories by total sales volume as
#measured by [items sold/$ values]
priority = "total_sale"
top_n = 9
top_categories = (
    sales_data
    .pivot_table(
        index="product_category_name_english",
        values=priority,
        aggfunc="sum"
        )
    .sort_values(by=priority, ascending=False)
    .head(n=top_n)
    .index.tolist()
    )

plot_data = sales_data.copy()

plot_data.loc[~plot_data["product_category_name_english"].isin(top_categories), "product_category_name_english"] = "Other"
#plot_data = plot_data[plot_data["product_category_name_english"].isin(top_categories)]

plot_data = plot_data.pivot_table(
    index="sale_month",
    values=priority,
    aggfunc="sum",
    columns="product_category_name_english"
    )
#sort columns so that the one with the biggest total is first
column_order = plot_data.sum().sort_values(ascending=True).index
plot_data = plot_data[column_order]

proportions = plot_data.div(plot_data.sum(axis=1), axis=0)
#%%
df = proportions
fig, ax = plt.subplots()

plt.stackplot(
    df.index,
    *df.T.values,
    labels=df.columns
    )
handles, labels = ax.get_legend_handles_labels()
plt.legend(
    fontsize=8,
    loc="upper left",
    handles=handles[::-1],
    labels=labels[::-1],
    )
plt.xticks(rotation=45)
plt.tight_layout()
plt.title(label=f"Top {top_n} product categories sales")

plt.savefig(project_root / "visuals" / "timeseries_sales.png", bbox_inches="tight")
plt.show()