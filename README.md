# Olist-Sales-Analysis
Analysis of publicly available sales data from Olist available on Kaggle at https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
<!-- 
Questions that are worth exploring
	Where are most of our sales coming from?
	Which products are the best/worst reviewed?
	Which products are making us the most money?
	Does the difference between estimated/actual delivery date correlate with review scores? Does it affect the odds of having a repeat customer?
	When in the year are the most sales made?
	Does the type of product sold vary across the seasons?

To Do list
-convert dates into proper datetimes so they can be analysed in data_cleaning.py
-complete temporal analysis
-->



<!--
This diagram is not of interest to stakeholders and is only for technical audience. Therefore it takes low priority and should go near the bottom
-->
## Relational diagram of raw datasets
```mermaid
erDiagram
%% List out tables
	olist_customers_dataset {
		string customer_id PK "each order has a unique customer id"
		string customer_unique_id PK "unique identifier of a customer"
		int customer_zip_code_prefix "first 5 digits of customer zip code"
		string customer_city "customer city name"
		string customer_state "customer state"
	}
	%%olist_geolocation_dataset {
	%%	int geolocation_zip_code_prefix "first 5 digits of zip code"
	%%	float geolocation_lat "latitude"
	%%	float geolocation_lng "longitude"
	%%	string geolocation_city "city name"
	%%	string geolocation_state "state"
	%%}
	olist_order_items_dataset {
		string order_id PK "order unique identifier"
		int order_item_id "number of items included in the same order"
		string product_id PK "product unique identifier"
		string seller_id PK "seller unique identifier"
		datetime shipping_limit_date "limit for seller to hand order to delivery"
		float price "item price"
		float freight_value "item freight value"
	}
	%%olist_order_payments_dataset {
	%%	string order_id PK "unique identifier of an order"
	%%	int payment_sequential "number of payment methods"
	%%	string payment_type "method of payment"
	%%	int payment_installments "number of installments"
	%%	float payment_value "transaction value"
	%%}
	%%olist_order_reviews_dataset {
	%%	string review_id UK "unique review identifier"
	%%	string order_id PK "unique order identifier"
	%%	int review_score "Review from 1 to 5"
	%%	string review_comment_title "Review title"
	%%	string review_comment_message "Review content"
	%%	datetime review_creation_date "Date that survey was sent to customer"
	%%	datetime review_answer_timestamp "Date survey was returned by customer"
	%%}
	%% "The core dataset" according to the kaggle page
	olist_orders_dataset {
		string order_id UK "unique identifier of the order"
		string customer_id PK "key to customer dataset. each order has unique value"
		string order_status
		datetime order_purchase_timestamp
		datetime order_approved_at "Payment approval timestamp"
		datetime order_delivered_carrier_date "When order was handed to logistic partner"
		datetime order_delivered_customer_date "When order arrived at customer"
		datetime order_estimated_delivery_date "Date that customer was told that the order would arrive at time of purchase"
	}
	%%olist_products_dataset {
	%%	string product_id UK "Unique product identifier"
	%%	%% "lenght" is not a typo that is how it appears in the dataset
	%%	string product_category_name "root category of product (portugese)" 
	%%	int product_name_lenght "Characters in product name"
	%%	int product_description_lenght "Characters in product description"
	%%	int product_photos_qty "number of product published photos"
	%%	int product_weight_grams
	%%	int product_length_cm
	%%	int product_height_cm
	%%	int product_width_cm
	%%}
	olist_sellers_dataset { 
		string seller_id UK "seller unique identifier"
		int seller_zip_code_prefix "first 5 digits of seller zip code"
		string seller_city
		string seller_state
	}
	%%product_category_name_translation {
	%%	string product_category_name
	%%	string product_category_name_english
	%%}

	%% List out connections between tables
	olist_geolocation_dataset ||..o{ olist_customers_dataset : customer_zip_code_prefix
	olist_geolocation_dataset ||..o{ olist_sellers_dataset : seller_zip_code_prefix
	olist_sellers_dataset ||..o{ olist_order_items_dataset : seller_id
	olist_products_dataset ||..o{ olist_order_items_dataset : product_id
	%%not certain the type of link between these datasets
	olist_orders_dataset }|--|{ olist_order_items_dataset : order_id
	olist_orders_dataset }|--|{ olist_order_payments_dataset : order_id
	olist_orders_dataset }|--|{ olist_order_reviews_dataset : order_id
	olist_orders_dataset }|--|{ olist_customers_dataset : customer_id

	%%product_category_name_translation ||..o{ olist_products_dataset : product_category_name

```
