#python -m streamlit run main.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_delivery_df(path = "./datasets/deliveries.jsonl"):
    delivery_df = pd.read_json(path, lines=True)
    delivery_df.set_index('purchase_id', inplace=True)
    delivery_df = delivery_df.replace([np.inf, -np.inf], np.nan)
    delivery_df = delivery_df.dropna(subset=["delivery_company", 'delivery_timestamp'])
    delivery_df['purchase_timestamp'] = pd.to_datetime(delivery_df['purchase_timestamp'])
    delivery_df['delivery_timestamp'] = pd.to_datetime(delivery_df['delivery_timestamp'])
    delivery_df['delivery_company'] = delivery_df["delivery_company"].astype(int)
    return delivery_df

def load_product_df(path = "./datasets/products.jsonl"):
    product_df = pd.read_json(path, lines=True)
    product_df.set_index('product_id', inplace=True)
    product_df = product_df.replace([np.inf, -np.inf], np.nan)
    product_df = product_df.dropna(subset=["price"])
    product_df = product_df[product_df.price >= 0]
    return product_df

if __name__ == "__main__":
    st.write("""
    # Sales analysis
    ## Analysed datasets:
    Deliveries dataset:""")
    delivery_df = load_delivery_df()
    st.dataframe(delivery_df)
    st.write('Products dataset:')
    product_df = load_product_df()
    st.dataframe(product_df)

    st.markdown("## Party time!")
    btn = st.button("Celebrate!")
    if btn:
        st.balloons()