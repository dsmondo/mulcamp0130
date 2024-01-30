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

    tab1, tab2, tab3 = st.tabs(['Most Reorderd', 'Sales by Products', 'Sales by Hour'])
    with tab1:      
        fig = px.bar(
        sum_top, x='product_name', y = 'total_reorders', title='Most Frequently Reordered',
        labels={'total_reorders': 'Total Rerder', 'product_name': 'Product Name'},
        color='product_name')
    
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = go.Figure()
        fig.add_trace(go.Histogram(
        x=top_10_orders['product_name'], 
        marker_color='#A0A0FF'))

        fig.update_layout(
            title='Sales By Products',
            xaxis_title='Product Name', 
            yaxis_title='Count' 
        )

        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = px.histogram(
        orders, x='order_hour_of_day', title='Sales Per Hour',
        labels={'order_hour_of_day': 'Order Hour', 'Count': 'Count'})
    
        st.plotly_chart(fig, use_container_width=True)
    #-----------------------------------------------------------
    # KPI
    kpi1, kpi2, kpi3 = st.columns(3)   

    # 가장 판매량 높은 dept
    merged = pd.merge(order_prod, products, on='product_id')
    dep_sales = merged.groupby('department_id')['order_id'].count().reset_index(name='total_sales')
    sales_max = dep_sales.sort_values(by='total_sales', ascending=False).head(1)
    # st.table(sales_max[['department_id', 'dep_sales']])
    
    # kpi1.metric(
    # label="Top Dept ⏳",
    # value=sales_max,
    # delta=sales_max - 10,
    # )

    # 구매량에 따른 VIP고객 선정
    # sum = orders.groupby('user_id')['order_number'].sum().reset_index(name='sum')
    # max_sale = sum.sort_values(by='sum', ascending=False).head(1)

    # kpi2.metric(
    #     label="VIP Customer 💍",
    #     value=max_sale,
    #     delta=-10 + max_sale,
    # )

    # kpi3.metric(
    #     label="A/C Balance ＄",
    #     value=f"$ {round(balance,2)} ",
    #     delta=-round(balance / count_married) * 100,
    # )

if __name__ == "__main__":
    main()

