# import urllib.request
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
# import altair

df = pd.read_csv('vehicles_us.csv')
df["brand"] = df['model'].str.split().str[0]
brands = df.brand.unique()
brands.sort()

# urllib.request.urlretrieve(
#    'http://koreabizwire.com/wp/wp-content/uploads/2018/11/AA.16823048.1.jpg',
#    "my_img.jpg")
img = Image.open("my_img.jpg")

st.title('Used cars DB')
st.image(img)
st.subheader('Use this app to learn about used cars market')

st.sidebar.caption(':red[Choose your parameters here]')
year_range = st.sidebar.slider(
    "What is your year range?",
    min_value=1900,
    max_value=2023,
    value=(1990, 2010))
year_range = list(range(year_range[0], year_range[1]+1))

price_range = st.sidebar.slider(
    "What is your price range?",
    value=(0, 375000), step=500)

selected_brands = st.sidebar.multiselect(
    'Select brand of car',
    brands, brands)


filtered_df = df[df['price'] <= price_range[1]]
filtered_df = filtered_df[filtered_df['price'] >= price_range[0]]
filtered_df = filtered_df[filtered_df.model_year.isin(year_range)]
filtered_df = filtered_df[filtered_df.brand.isin(selected_brands)]

fig2 = px.scatter(filtered_df, x="odometer", y="price", color='brand',
                  title='Dependence of price on car mileage',
                  range_y=(0, filtered_df.price.max()),
                  trendline="ols", trendline_scope="overall",
                  trendline_color_override="black")
st.write('Diagram 1.', fig2)

fig1 = px.histogram(filtered_df, x="brand", color='fuel',
                    title='Distribution of brands and fuel type')
st.write('Diagram 2.', fig1)

fig3 = px.histogram(filtered_df, x="model_year",
                    title='Distribution of years of manufacture of the car')
st.write('Diagram 3.', fig3)

fig = px.pie(filtered_df,  names='brand', hole=.3,
             title='Distribution of brands')
st.write('Diagram 4.', fig)
