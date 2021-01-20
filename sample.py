import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import geopandas as gpd
warnings.filterwarnings('ignore')

df = pd.read_csv('data/schools_combined.csv')

st.title("Public School Data in the Philippines")

my_page = st.sidebar.radio('Page Navigation', ['page 1', 'page 2', 'page 3', 'page 4'])

if my_page == 'page 1':
    # Add section header
    st.header("Data")
    st.subheader("Up to 2015")
    if st.checkbox('Show data', value=True):
        st.subheader('Data')
        data_load_state = st.text('Loading data...')
        st.write(df.head(20))
        data_load_state.markdown('Loading data...**done!**')

elif my_page == 'page 2':
    st.header("Enrollment by Region")
    option = st.selectbox(
        'Which region do you want to see?',
        df['region'].unique())
    'You selected: ', option
    grade_level = df[df.region == option].groupby("year_level")["enrollment"].sum()
    # indicates if plotting on the figues or on subplots
    fig = plt.figure(figsize=(8,6)) 

    # the main code to create the graph
    plt.bar(grade_level.index, grade_level.values) 

    # additional elements that can be customzed
    plt.title("Students in Public Schools", fontsize=16)
    plt.ylabel("Number of Enrollees", fontsize=12)
    plt.xlabel("Year Level", fontsize=12)
    year = ["grade 1","grade 2", "grade 3", "grade 4", "grade 5", "grade 6",
            "first year", "second year", "third year", "fourth year"]
    plt.xticks(range(len(grade_level.index)), year, rotation=45)

    # display graph
    plt.show()
    st.pyplot(fig)

elif my_page == 'page 3':
    st.header("Geospatioal Analysis of Schools")
    schools = gpd.read_file('data/phl_schp_deped/phl_schp_deped.shp')
    schools["x"] = schools.geometry.centroid.x
    schools["y"] = schools.geometry.centroid.y
    #st.write(schools.head(20))
    # Coordinates to show
    map_center = [14.583197, 121.051538]

    # Styling the map
    mymap = folium.Map(location=map_center, height=700, width=1000, tiles="OpenStreetMap", zoom_start=14)
    option_city = st.sidebar.selectbox(
        'Which city',
        schools["Division"].unique())
    'You selected: ', option_city
    city = option_city

    df_city = schools[schools["Division"]==city]

    for i in np.arange(len(df_city)):
        lat = df_city["y"].values[i]
        lon = df_city["x"].values[i]
        name = df_city["School"].values[i]
        folium.Marker([lat, lon], popup=name).add_to(mymap)
    folium_static(mymap)

elif my_page == 'page 4':
    st.title("Geospatioal Analysis of Schools : st.map")
    schools = gpd.read_file('data/phl_schp_deped/phl_schp_deped.shp')
    # to plot a map using st.map, you need a column names lon and lat
    schools["lon"] = schools.geometry.centroid.x
    schools["lat"] = schools.geometry.centroid.y
    st.map(schools.head(10))

