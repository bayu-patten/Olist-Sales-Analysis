# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 20:50:30 2026

Investigate variation in product type sold over time and seasonally
See variation in count of items sold and in $ value

@author: imbkp20
"""
#%%
import matplotlib.pyplot as plt
from sales_data import sales_data, project_root

#%% construct data to be used for plots
#we only want to deal with data regarding completed orders
sales_data = sales_data[sales_data["order_status"] == "delivered"]
sales_data = sales_data[sales_data["order_delivered_customer_date"].notna()]

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
top_n = 10
for priority in ["total_sale", "order_item_id"]:
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
    #%% Plot how the sales of each product category varied over time
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
        bbox_to_anchor=(1.02, 1),
        handles=handles[::-1],
        labels=labels[::-1],
        )
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.title(label=f"Top {top_n} product categories by {priority}")
    
    plt.savefig(project_root / "visuals" / f"timeseries_{priority}.png", bbox_inches="tight")
    plt.show()
    
    #%% bar charts of total sales by each priority
    fig,ax = plt.subplots()
    bar_chart_data = (
        sales_data
        .pivot_table(
            index="product_category_name_english",
            values=priority,
            aggfunc="sum"
            )
        .sort_values(by=priority, ascending=False)
        .head(n=top_n)
        )
    
    plt.barh(
        y=bar_chart_data.index,
        width=bar_chart_data[priority]
        )
    ax.invert_yaxis()
    plt.title(label=f"Top {top_n} product categories by {priority}")
    
    plt.savefig(project_root / "visuals" / f"top_categories_{priority}.png", bbox_inches="tight")
    plt.show()
    
    
    