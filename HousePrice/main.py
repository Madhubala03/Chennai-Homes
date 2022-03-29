import streamlit as st
import pickle
import pandas as pd
import plotly.express as px
from babel.numbers import format_currency
data=pd.read_csv("cleaned.csv")
model = pickle.load(open('model_pkl','rb'))
# Create a page dropdown
page = st.sidebar.selectbox("Select One", ["Predict Price", "Explore",'Creator'])
if page == "Predict Price":
    st.title('Price Prediction')
    AREA = st.selectbox("Select an Area ",data.AREA.unique())
    if AREA == 'Chrompet':
        AREA = 2
    elif AREA == 'Karapakkam':
        AREA  = 4
    elif AREA == 'KK Nagar':
        AREA = 3
    elif AREA == 'Anna Nagar':
        AREA = 1
    elif AREA == 'Adyar':
        AREA = 0
    elif AREA == 'T Nagar':
        AREA = 5
    else:
        AREA = 6

    INT_SQFT = st.slider("SQFT Required",int(data.INT_SQFT.min()),int(data.INT_SQFT.max()))

    N_BEDROOM = st.slider("No of Bedrooms",int(data.N_BEDROOM.min()),int(data.N_BEDROOM.max()))

    N_BATHROOM = st.slider("No of Bathrooms",int(data.N_BATHROOM.min()),int(data.N_BATHROOM.max()))

    N_ROOM = st.slider("No of Rooms",int(data.N_ROOM.min()),int(data.N_ROOM.max()))

    PARK_FACIL = st.radio("Parking Area",data.PARK_FACIL.unique())
    if PARK_FACIL == 'Yes':
        PARK_FACIL = 1
    else:
        PARK_FACIL = 0

    #Coverting MZZONe categorical to numerical
    MZZONE = st.selectbox("Chennai Zone Preference",data.MZZONE.unique())
    if MZZONE == 'A':
        MZZONE = 0
    elif MZZONE == 'RH':
        MZZONE = 3
    elif MZZONE == 'RL':
        MZZONE = 4
    elif MZZONE == 'I':
        MZZONE = 2
    elif MZZONE == 'C':
        MZZONE = 1
    else:
        MZZONE = 5

    BUILDTYPE = st.radio("Purpose",data.BUILDTYPE.unique())

    if BUILDTYPE == 'House':
        BUILDTYPE = 1
    elif BUILDTYPE == 'Others':
        BUILDTYPE = 2
    else:
        BUILDTYPE = 0
    
    
    
    STREET = st.selectbox("Access TO THE Building",data.STREET.unique())

    if STREET == 'Gravel':
        STREET = 0
    elif STREET == 'Paved':
        STREET = 2
    else:
        STREET = 1

    input = pd.DataFrame([[INT_SQFT,BUILDTYPE,MZZONE,AREA,N_BEDROOM,PARK_FACIL,N_BATHROOM,STREET,N_ROOM]],columns=['INT_SQFT','BUILDTYPE','MZZONE','AREA','N_BEDROOM','PARK_FACIL',N_BATHROOM,STREET,N_ROOM],index=['index'])
                        
                        
    #st.dataframe(input)

    valu = model.predict(input)
    low=int(valu-(valu*0.02))
    low = format_currency(low, 'INR', locale='en_IN')


    high=int(valu+(valu*0.02))
    high = format_currency(high, 'INR', locale='en_IN')

    #print('Estimated value is:',low , 'to', high)


    if st.button(" Get Price",help="Click to predict the price"):
        st.markdown("<h1 style='text-align: center; color: grey;'>Predicted House Price Range</h1>", unsafe_allow_html=True)
        st.write("😀😀😀😀😀😀😀😀😀😀",  low , 'to', high   ,"😀😀😀😀😀😀😀😀😀")



elif page == "Explore":
    st.write('Area with Highest Sales')
    fig=px.bar(data,x='AREA')
    st.plotly_chart(fig, use_container_width=True)
else:
   st.write('Display details of page 3')
