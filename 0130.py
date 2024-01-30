# -*- coding:utf-8 -*-
import numpy as np 
import pandas as pd
import streamlit as st
import seaborn as sns
import plotly.graph_objects as go 
import plotly.express as px

#garbage collector
import gc
gc.enable()

@st.cache_data
def load_orders():
    orders = pd.read_csv('data/sample_order1.csv')
    return orders

@st.cache_data
def load_products():
    products = pd.read_csv('data/sample_products1.csv')
    return products

# @st.cache_data
# def load_aisles():
#     PATH = 'instacart-market-basket-analysis/'
#     aisles = pd.read_csv(PATH + 'aisles.csv/aisles.csv')
#     return aisles

# @st.cache_data
# def load_departments():
#     PATH = 'instacart-market-basket-analysis/'
#     departments = pd.read_csv(PATH +'departments.csv/departments.csv')
#     return departments

@st.cache_data
def load_order_prod():
    order_prod = pd.read_csv('data/sample_order_prod1.csv')
    return order_prod

def main():
    import os
    for dirname, _, filenames in os.walk('kaggle/input'):
        for filename in filenames:
            print(os.path.join(dirname, filename))

    orders = load_orders()
    # aisles = load_aisles()
    products = load_products()
    # dep = load_departments()
    order_prod = load_order_prod()

    order_new = orders.merge(order_prod)
    order_new = order_new.merge(products)

    st.header('Instacart Market Basket Analysis')

    #----------------------------------------------------------
    # 판매량 TOP10 상품 추출
    
    # Calculate the number of products in each order
    order_counts = order_new.groupby('order_id').size().reset_index(name='product_count')

    # Sort orders based on the number of products and get the top 10
    top_10_orders = order_counts.sort_values(by='product_count', ascending=False).head(10)

    top_10_orders = pd.merge(order_new, top_10_orders, on='order_id')
    # st.header('top_10_orders')
    # st.write(top_10_orders.head(30))

    # top_10_orders_with_names = pd.merge(top_10_orders, order_new[['order_id', 'product_name']], on='order_id')
    
    # st.header('top_10_orders_with_names')
    # st.write(top_10_orders_with_names.head())
    
    #-----------------------------------------------------------
    # 리오더 상품 총합계산
    sum = order_prod.groupby('product_id')['reordered'].sum().reset_index(name='total_reorders')
    sum_w_prod_name = pd.merge(sum, products, on='product_id')
    sum_top = sum_w_prod_name.sort_values(by='total_reorders', ascending=False).head()
    
    #-----------------------------------------------------------
    # order_prod[order_prod['add_to_cart_order']==1]

    tab1, tab2, tab3 = st.tabs(['Most Reorderd', 'Sales by Products', 'Sales by Hour'])
    with tab1:      
        fig = px.bar(
        sum_top, x='product_name', y = 'total_reorders', title='Most Frequently Reordered',
        labels={'total_reorders': 'Total Rerder', 'product_name': 'Product Name'})
    
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.histogram(
        top_10_orders, x='product_name', title='Sales By Products',
        labels={'product_name': 'Product Name', 'count': 'Count'})
    
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = px.histogram(
        orders, x='order_hour_of_day', title='Sales Per Hour',
        labels={'order_hour_of_day': 'Order hour', 'Count': 'Count'})
    
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()

