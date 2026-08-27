# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 14:15:25 2026

Script to provide pandas dataframe and project root for other scripts to import
from to avoid repetition

@author: imade
"""

import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

sales_data = pd.read_csv(project_root / "data" / "processed" / "merged_data.csv")

sales_data = sales_data.drop("product_category_name", axis="columns")

for datecol in [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "shipping_limit_date"
        ]:
    sales_data[datecol] = pd.to_datetime(sales_data[datecol])
    
sales_data["sale_month"] = (
    sales_data["order_delivered_customer_date"]
    .dt.to_period('M')
    .dt.to_timestamp()
    )

sales_data["total_sale"] = sales_data["price"]*sales_data["order_item_id"]
