import streamlit as st
import pickle
import pandas as pd
import plotly.express as px
from babel.numbers import format_currency
from PIL import Image
data=pd.read_csv("cleaned.csv")
model = pickle.load(open('model_pkl','rb'))
# Create a page dropdown
image = Image.open('logo.jpg')
st.sidebar.image(image,width=124)
st.sidebar.title("ChennaiHomes")
col1, col2 = st.columns( [0.5, 0.5])
with col1:
    st.title("ChennaiHomes")   
with col2:
    st.image(image,  width=150)
page = st.sidebar.selectbox("Select One", ['Home',"Predict Price", "Explore",'Creator'])
if page == "Home":
    st.title('Welcome to ChennaiHomes')
    st.subheader('ChennaiHomes is a platform where you can explore the statistics of Sales happened across Chennai over the years 2013-2017 and also predict the current price range of your Dream Homes')
if page == "Predict Price":
    st.title('Price Prediction')
    AREA = st.selectbox("Select an Area ",data.AREA.unique())
    if AREA == 'Chrompet':
        grouped=data[data['AREA']=='Chrompet']
        AREA = 2
    elif AREA == 'Karapakkam':
        grouped=data[data['AREA']=='Karapakkam']
        AREA  = 4
    elif AREA == 'KK Nagar':
        grouped=data[data['AREA']=='KK Nagar']
        AREA = 3
    elif AREA == 'Anna Nagar':
        grouped=data[data['AREA']=='Anna Nagar']
        AREA = 1
    elif AREA == 'Adyar':
        grouped=data[data['AREA']=='Adyar']
        AREA = 0
    elif AREA == 'T Nagar':
        grouped=data[data['AREA']=='T Nagar']
        AREA = 5
    elif AREA == 'Velachery':
        grouped=data[data['AREA']=='Velachery']
        AREA = 6

    INT_SQFT = st.slider("SQFT Required",int(data.INT_SQFT.min()),int(data.INT_SQFT.max()))

    N_BEDROOM = st.slider("No of Bedrooms",int(data.N_BEDROOM.min()),int(data.N_BEDROOM.max()))

    N_BATHROOM = st.radio("No of Bathrooms",data.N_BATHROOM.unique())

    N_ROOM = st.slider("No of Rooms",int(data.N_ROOM.min()),int(data.N_ROOM.max()))

    PARK_FACIL = st.radio("Parking Area",data.PARK_FACIL.unique())
    if PARK_FACIL == 'Yes':
        PARK_FACIL = 1
    else:
        PARK_FACIL = 0

    #Coverting MZZONe categorical to numerical
    MZZONE = st.selectbox("Chennai Zone Preference",grouped.MZZONE.unique())
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
        st.markdown("<h1 style='text-align: center; color: Black;'>Predicted House Price Range</h1>", unsafe_allow_html=True)
        st.write("😀😀😀😀😀😀😀😀😀😀",  low , 'to', high   ,"😀😀😀😀😀😀😀😀😀")
        st.snow()


elif page == "Explore":
    st.write('**Area wise Sales**')
    fig=px.bar(data,x='AREA',color='AREA')
    fig.update_traces(marker_line_width = 0,selector=dict(type="bar"))
    st.plotly_chart(fig, use_container_width=True)
    expander = st.expander("Insights")
    expander.write("""The chart above shows No of Sales happened in each Area respectively. As you can see 
    **Chrompet** has made the most sales""")

    st.write("**Sales happend based on Parking Facility**")
    fig1=px.bar(data,x='AREA',barmode='group',color='PARK_FACIL')
    fig1.update_traces(marker_line_width = 0,selector=dict(type="bar"))
    st.plotly_chart(fig1, use_container_width=True)
    expander = st.expander("Insights")
    expander.write("""The chart above shows No of Sales made based on the parking facillity available. We can see that
    there is no bias based on the parking facility""")

    st.write("**Sales happend based on the Type of Building**")
    fig2=px.bar(data,x='AREA',barmode='group',color='BUILDTYPE')
    fig2.update_traces(marker_line_width = 0,selector=dict(type="bar"))
    st.plotly_chart(fig2, use_container_width=True)
    expander = st.expander("Insights")
    expander.write("""The chart above shows No of Sales made based on the Building Type""")
 

elif page == "Creator":
    st.title('Creator Profile')
    st.write('**App Creator:** Madhubala A')
    st.write('**Mail Id:** madhu.masy@gmail.com')
    st.write("**Linked In:** https://www.linkedin.com/in/madhubala-anbalagan/")
