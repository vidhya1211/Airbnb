import streamlit as st
from streamlit_option_menu import option_menu
import pymongo
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import ast
import pymysql
from PIL import Image
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.express as px

connection = pymysql.connect(
        host='localhost',
        user='root',
        password='DataScience@12',
        database="Airbnb",
        port=3306
    )
cursor=connection.cursor()

cursor=connection.cursor()
cursor.execute('''select data1.*, data_host1.*, data_address1.*, data_availability_1.* from data1
JOIN data_host1 ON data1._id = data_host1._id
JOIN data_address1 ON data1._id = data_address1._id
JOIN data_availability_1 ON data1._id = data_availability_1._id''')
rows=cursor.fetchall()

column_names=[desc[0] for desc in cursor.description]

df=pd.DataFrame(rows,columns=column_names)

df=df.loc[:,~df.columns.duplicated()]

st.set_page_config(layout= "wide")
st.title("AIRBNB DATA ANALYSIS")
st.write("")

with st.sidebar:
    select= option_menu("Main Menu", ["Home", "Data Exploration", "Detail"])
if select=="Home":
    col1, col2=st.columns(2)
    with col1:
        image1 = Image.open("D:\\project\\airbnb project image.jpg")
        st.image(image1)
    with col2:
        st.header("Airbnb")
        st.write("")
        st.write('''***Airbnb is an online marketplace that connects people who want to rent out
                    their property with people who are looking for accommodations,
                    typically for short stays. Airbnb offers hosts a relatively easy way to
                    earn some income from their property.Guests often find that Airbnb rentals
                    are cheaper and homier than hotels.***''')
    

if select=="Data Exploration":
    if select == "Data Exploration":
        tab1, tab2, tab3 = st.tabs(["***PRICE ANALYSIS***","***AVAILABILITY ANALYSIS***","***LOCATION BASED***"])
        with tab1:
            st.title("**PRICE ANALYSIS**")
            col1,col2=st.columns(2)
            with col1:
            
                country = st.selectbox("Select the Country", df["country"].unique())

                df1= df[df["country"] == country]
                df1.reset_index(drop= True, inplace= True)

                room_type= st.selectbox("Select the Room Type",df1["room_type"].unique())
                
                df2= df1[df1["room_type"] == room_type]
                df2.reset_index(drop= True, inplace= True)

                df_bar= pd.DataFrame(df2.groupby("property_type")[["price","review_scores","number_of_reviews"]].sum())
                df_bar.reset_index(inplace= True)

                fig_bar= px.bar(df_bar, x='property_type', y= "price", title= "PRICE FOR PROPERTY_TYPES",hover_data=["number_of_reviews","review_scores"],color_discrete_sequence=px.colors.sequential.Redor_r, width=600, height=500)
                st.plotly_chart(fig_bar)
            with col2:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")

                fig_scatter = px.scatter(df2,x="amenities_count",y="price",title="PRICE FOR AMENITIES COUNT",hover_data=["name", "property_type", "review_scores"],  
                                            width=600,height=400, opacity=0.6, color_discrete_sequence=["#636EFA"])
                st.plotly_chart(fig_scatter)

            col1,col2=st.columns(2)
            with col1:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")

                df1_bar = df2.groupby("bed_type")["price"].mean().reset_index()
                fig_bar = px.bar(df1_bar, x="bed_type",y="price",title="💰 Average Price by Bed Type",color="bed_type",text="price",
                                    color_discrete_sequence=px.colors.sequential.Sunset_r, labels={"price": "Average Price", "bed_type": "Bed Type"},width=700, height=500)

                st.plotly_chart(fig_bar)
            
            with col2:
                country = st.selectbox("Select Country", df["country"].dropna().unique(), key="country_select")

                df_country = df[df["country"] == country].copy()
                df3 = df_country.groupby("room_type")["price"].mean().reset_index()

                fig_pie = px.pie(df3, names="room_type", values="price", title="💰 Total Price by Room Type", color="room_type",
                    color_discrete_sequence=px.colors.sequential.RdBu)

                st.plotly_chart(fig_pie)

        with tab2:
            st.title("***AVAILABILITY ANALYSIS***")
            
            available = ["room_type", "availability_30", "availability_60", "availability_90", "availability_365"]
            df4= df[available].dropna()

            df5 = df4.groupby("room_type")[["availability_30", "availability_60", "availability_90", "availability_365"]].mean().reset_index()

            df_long = df5.melt(id_vars="room_type", 
                                        value_vars=["availability_30", "availability_60", "availability_90", "availability_365"],
                                        var_name="Availability_Window", 
                                        value_name="Average_Availability")

            fig_avail = px.bar(data_frame=df_long,x="room_type", y="Average_Availability", color="Availability_Window", barmode="group",
                title="📅 Average Availability days by Room Type", labels={"room_type": "Room Type", "Average_Availability": "Avg. Availability (days)"},
                color_discrete_sequence=px.colors.qualitative.Set2)

            st.plotly_chart(fig_avail)

            col1,col2=st.columns(2)
            with col1:
                avg_available_30 = df.groupby('country')['availability_30'].mean().reset_index()
                
                fig_bar= px.bar(avg_available_30, x='country', y='availability_30',
                            title='Average Availability Over 30 Days by Country',
                            labels={'availability': 'Avg Availability (30 days)', 'country': 'Country'})

                st.plotly_chart(fig_bar)

            with col2:
                avg_available_365 = df.groupby('country')['availability_365'].mean().reset_index()
                
                fig_pie = px.pie(avg_available_365, names='country', values='availability_365',
                            title='Average Availability Over 365 Days by Country',
                            labels={'availability': 'Avg Availability (365 days)', 'country': 'Country'})

                st.plotly_chart(fig_pie)
        with tab3:
            st.title("***LOCATION BASED***")
            country_availability = df.groupby("country")["availability_365"].mean().reset_index()

            fig_map1 = px.choropleth(country_availability,locations="country",locationmode="country names",color="availability_365",color_continuous_scale="Blues",range_color=(0, 365),
                                labels={'availability_365': 'Avg Availability (days)'},  title="Average Airbnb Availability (365 Days) by Country")
            st.plotly_chart(fig_map1)

            room_types = df['room_type'].unique()
            selected_room = st.selectbox("Select Room Type", room_types)

            room_type_df= df[df['room_type'] == selected_room]

            df5 = room_type_df.groupby("country")["availability_365"].mean().reset_index()

            st.title(f"Avg Availability for {selected_room} by Country")

            fig_map2= px.choropleth(df5, locations="country", locationmode="country names", color="availability_365", color_continuous_scale="Blues", range_color=(0, 365), labels={"availability_365": "Avg Availability (days)"},
                                    title=f"365-Day Availability of {selected_room}s Across Countries")

            st.plotly_chart(fig_map2)

            st.title("Airbnb Availability by Accommodation Size and Country")

            accommodate_options = sorted(df["accommodates"].unique())
            Guest= st.selectbox("Number of Guest", accommodate_options)

            accommodate_df = df[df["accommodates"] == Guest]

            df6 = accommodate_df.groupby("country")["availability_365"].mean().reset_index()

            fig_map3 = px.choropleth(df6, locations="country", locationmode="country names", color="availability_365", color_continuous_scale="YlGnBu",
                                range_color=(0, 365), labels={"availability_365": "Avg Availability (days)"})

            st.plotly_chart(fig_map3)

        

if select=="Detail":
    st.header("ABOUT THIS PROJECT")

    st.subheader(":red[1. Data Collection:]")

    st.write('''***Gather data from Airbnb's public API or other available sources.
        Collect information on listings, hosts, reviews, pricing, and location data.***''')
    
    st.subheader(":red[2. Data Cleaning and Preprocessing:]")

    st.write('''***Clean and preprocess the data to handle missing values, outliers, and ensure data quality.
        Convert data types, handle duplicates, and standardize formats.***''')
    
    st.subheader(":red[3. Exploratory Data Analysis (EDA):]")

    st.write('''***Conduct exploratory data analysis to understand the distribution and patterns in the data.
        Explore relationships between variables and identify potential insights.***''')
    
    st.subheader(":red[4. Visualization:]")

    st.write('''***Create visualizations to represent key metrics and trends.
        Use charts, graphs, and maps to convey information effectively.
        Consider using tools like Matplotlib or Plotly for visualizations.***''')
    
    st.subheader(":red[5. Geospatial Analysis:]")

    st.write('''***Utilize geospatial analysis to understand the geographical distribution of listings.
        Map out popular areas, analyze neighborhood characteristics, and visualize pricing variations.***''')
