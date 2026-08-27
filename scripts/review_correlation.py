# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 14:10:27 2026

Investigate if review scores correlate with things like late deliveries

@author: imade
"""

import matplotlib.pyplot as plt
from sales_data import sales_data, project_root
from scipy.stats import pearsonr




#calculate the difference between esitmated and real delivery date
#positive number means it was LATE
#negative number means it was on time
sales_data["delivery_real_estimate_diff"] = (
    sales_data["order_delivered_customer_date"]
    -sales_data["order_estimated_delivery_date"]
    ).dt.total_seconds() / (24 * 60 * 60)

sales_data = (
    sales_data
    .drop_duplicates(subset="order_id")
    .dropna(subset=["review_score", "delivery_real_estimate_diff"], how="any")
    )

#%% compute statistical significance
r, p = pearsonr(sales_data["delivery_real_estimate_diff"], sales_data["review_score"])

print("Correlation:", r)
print("p-value:", p)

#%% draw boxplot
labels = [1,2,3,4,5]
plot_data = [
    sales_data.loc[sales_data["review_score"] == score, "delivery_real_estimate_diff"]
    for score in labels]

fig, ax = plt.subplots()
plt.boxplot(
    x=plot_data,
    labels=labels,
    vert=False,
    )

ax.set_xlim(-50,50)
ax.set_xlabel("Days Delivery was Late by")
ax.set_ylabel("Review Score")
plt.title(label="Review Score vs Delivery Tardiness")
plt.text(
    x=-50,
    y=-0.75,
    s=f"Correlation: {round(r,2)}\np-value: {p}"
    )

plt.savefig(
    project_root / "visuals" / "reviews_delivery_lateness.png",
    bbox_inches="tight")
plt.show()

#%%
#the 0.0 p value tells us that indeed delays make for negative reviews
#now a question worth asking is "do negative reviews make for non-repeat
#customers?"
