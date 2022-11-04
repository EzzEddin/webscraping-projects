import requests

# Data manipulation
import pandas as pd
import numpy as np

# Create sample keyword dataframe from dict
data3 = {'part number': [123456, 234567, 345678, 456789], 'search keyword': ['apple', 'banana', 'orange', 'mango']}

df3 = pd.DataFrame.from_dict(data3)
print(df3)

# Input API parameters
for i in df3['search keyword']:
    Shopee_url = 'https://shopee.com.my'
    keyword_search = i
    headers = {
     'User-Agent': 'Chrome',
     'Referer': '{}search?keyword={}'.format(Shopee_url, keyword_search)
    }
    url = 'https://shopee.com.my/api/v2/search_items/?by=relevancy&keyword={}&limit=100&newest=0&order=desc&page_type=search'.format(keyword_search)

    # Shopee API request
    r = requests.get(url, headers = headers).json()

    # Shopee scraping script
    title_list = []
    min_price_after_discount_list = []
    standard_retail_price_list = []
    shop_location_list = []
    shop_id_list = []
    item_id_list = []
    for item in r['items']:
        title_list.append(item['name'])
        min_price_after_discount_list.append(item['price_min'])
        standard_retail_price_list.append(item['price_min_before_discount'])
        shop_location_list.append(item['shop_location'])
        shop_id_list.append(item['shopid'])
        item_id_list.append(item['itemid'])

# Define a dictionary from web scraped data
data2 = {'Part Number': "123456",
        'Product Name': title_list,
        'Min Price After Discount': min_price_after_discount_list,
        'Extracted Standard Retail Price': standard_retail_price_list,
        'Seller Location': shop_location_list,
        'Seller ID': shop_id_list,
        'Product ID': item_id_list,
        'Product URL': "https://shopee.com.my/product/shopid/itemid/"
       }

# Convert the dictionary into DataFrame
df2 = pd.DataFrame(data2)