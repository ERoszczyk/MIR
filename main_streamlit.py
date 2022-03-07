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

def load_sessions_df(path = "./datasets/sessions.jsonl"):
    sessions_df = pd.read_json(path, lines=True)
    sessions_df.set_index('session_id', inplace=True)
    return sessions_df

def show_plot_for_years(years, x_list, y_list, title, rotation=0):
    years = list(years)
    years.sort()
    N = len(x_list)
    ind = np.arange(N) 
    width = 0.25
    plt.figure(figsize = (20, 7))
    plots = []
    for index, y in enumerate(y_list):
        plots.append(plt.bar(ind+width*index, y, width))
    plt.legend(plots, years)
    plt.xticks(ind+width, x_list, rotation=rotation)
    plt.title(title)
    st.pyplot(fig=plt)

if __name__ == "__main__":
    st.write("""
    # Analiza sprzedaży
    ## Analizowane zbiory danych:
    Zbiór danych dostaw:""")
    delivery_df = load_delivery_df()
    st.dataframe(delivery_df)
    st.write('Zbiór danych produktów:')
    product_df = load_product_df()
    st.dataframe(product_df)
    st.write('Zbiór danych sesji użytkowników:')
    sessions_df = load_sessions_df()
    st.dataframe(sessions_df)

    st.write('## Wykresy danych:')

    years = delivery_df["purchase_timestamp"].dt.year.value_counts().to_dict().keys()
    months = range(1, 13)

    df_list = []
    for index, year in enumerate(years):
        delivery_year =  delivery_df[delivery_df.purchase_timestamp.dt.year.eq(year)]
        df = delivery_year.groupby(delivery_year["purchase_timestamp"].dt.month)["purchase_timestamp"].count().to_dict()
        
        for num_month in months:
            if num_month not in df.keys(): 
                df[num_month] = 0 
                
        df_list.append([j for _,j in sorted(df.items())])

    show_plot_for_years(years, months, df_list, "Liczba zamówień w zależności od miesiąca")
    
    purchase_from_category_df = pd.merge(sessions_df[sessions_df['event_type'] == "BUY_PRODUCT"], product_df, on='product_id', how='inner')
    years = purchase_from_category_df["timestamp"].dt.year.value_counts().to_dict().keys()
    categories = purchase_from_category_df.groupby(purchase_from_category_df["category_path"])["category_path"].count().to_dict().keys()
    df_list = []
    for index, year in enumerate(years):
        purchase_from_category_year = purchase_from_category_df[purchase_from_category_df.timestamp.dt.year.eq(year)]
        df = purchase_from_category_year.groupby(purchase_from_category_year["category_path"])["category_path"].count().to_dict()
        month_amount = len(purchase_from_category_year.groupby(purchase_from_category_year['timestamp'].dt.month)["timestamp"].count())
        df = dict(sorted(df.items())).values()
        df_list.append(np.divide(list(df), month_amount))

    show_plot_for_years(years, categories, df_list, "Średnia liczba zamówień z danej kategorii w zależności od roku", rotation=90)
    
    view_from_category_df = pd.merge(sessions_df[sessions_df['event_type'] == "VIEW_PRODUCT"], product_df, on='product_id', how='inner')
    years = view_from_category_df["timestamp"].dt.year.value_counts().to_dict().keys()
    categories = view_from_category_df.groupby(view_from_category_df["category_path"])["category_path"].count().to_dict().keys()
    df_list = []
    for index, year in enumerate(years):
        view_from_category_year = view_from_category_df[view_from_category_df.timestamp.dt.year.eq(year)]
        df = view_from_category_year.groupby(view_from_category_year["category_path"])["category_path"].count().to_dict()
        month_amount = len(view_from_category_year.groupby(view_from_category_year['timestamp'].dt.month)["timestamp"].count())
        df = dict(sorted(df.items())).values()
        df_list.append(np.divide(list(df), month_amount))

    show_plot_for_years(years, categories, df_list, "Średnia liczba wyświetleń produktów z dnaej kategorii w zależności od roku", rotation=90)
    st.markdown("## Party time!")
    click = st.button("Celebrate!")
    if click:
        st.balloons()