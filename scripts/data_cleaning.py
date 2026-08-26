from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parent.parent

raw_data = project_root / "data" / "raw"

#%% Reading in raw datasets
customers = pd.read_csv(raw_data / "olist_customers_dataset.csv")
geolocation = pd.read_csv(raw_data / "olist_geolocation_dataset.csv")
order_items = pd.read_csv(raw_data / "olist_order_items_dataset.csv")
order_payments = pd.read_csv(raw_data / "olist_order_payments_dataset.csv")
reviews = pd.read_csv(raw_data / "olist_order_reviews_dataset.csv")
orders = pd.read_csv(raw_data / "olist_orders_dataset.csv")
products = pd.read_csv(raw_data / "olist_products_dataset.csv")
sellers = pd.read_csv(raw_data / "olist_sellers_dataset.csv")
translation = pd.read_csv(raw_data / "product_category_name_translation.csv")

#%% Tidy tables before merging

#geolocation has many entries for a single zip code prefix so we will just
#drop all the duplicates and assume its fine
geolocation = geolocation.drop_duplicates(subset="geolocation_zip_code_prefix")

#%%
#order_items has fewer order_id values than the orders dataset.
#which orders are missing?

#%%
#reviews has more entries than unique order_id values
reviews_repeat_order_ids = reviews[reviews["order_id"].duplicated(keep=False)]
#someone can drop multiple reviews for the same order

#%%
#are there are orders that dont appear in order_items?
order_no_items = orders[~orders["order_id"].isin(order_items["order_id"])]
order_with_items = orders[orders["order_id"].isin(order_items["order_id"])]
#these are mostly the orders which are unavailable order_status and some
#of the cancellations
#%% Crudely link all the data together for analysis
final_data = (
    orders
    #add data about the customer
    .merge(customers, on="customer_id", how="left")
    #customer dataset already has info on state and city so merging
    #the geolocation on is only necessary if we want lat/lng which we
    #will leave for now
#    .merge(
#        geolocation
#        .rename(
#            #columns={
#                "geolocation_zip_code_prefix":"customer_zip_code_prefix",
#                "geolocation_lat":"customer_lat",
#                "geolocation_lng":"customer_lng",
#                "geolocation_city":"customer_city",
#                "geolocation_state":"customer_state"
#                }
#            ),
#        on="customer_zip_code_prefix",
#        how="left"
#        )
    #do an outer join becasue we can filter later to just orders with item
    #data or drop duplicated key values if we only want one representative
    .merge(order_items, on="order_id", how="outer") #might duplicate values
    
    .merge(sellers, on="seller_id", how="outer")
    .merge(products, on="product_id", how="outer")
    #translations do not need the outer merge as we will not be interested
    #in a translation dataset
    .merge(translation, on="product_category_name", how="left")
    #will not merge reviews data on as it will duplicate values and be useless
    )
final_data.to_csv(
    project_root / "data" / "processed" / "merged_data.csv",
    index=False
    )







