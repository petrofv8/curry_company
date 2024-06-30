#importando as bibliotecas 
from haversine import haversine
import plotly.express as px 
import plotly.graph_objects as go 
import numpy as np 

# bibliotecas necessárias 
import pandas as pd 
from datetime import datetime
from dateutil.parser import parse
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static


#============================================================================
#Funções 
#============================================================================

def clean_code(df1):
    """
    Esta função tem a responsabilidade de limpar o dataframe
    """
    #removendo a linhas NaN
    linhas_trash = df1['Delivery_person_Age']!= 'NaN '
    df1 =df1.loc[linhas_trash,:].copy()
    linhas_trash = df1['Delivery_person_Ratings']!= 'NaN '
    df1 =df1.loc[linhas_trash,:].copy()
    linhas_trash = df1['multiple_deliveries']!= 'NaN '
    df1 =df1.loc[linhas_trash,:].copy()
    linhas_trash = df1['City']!= 'NaN'
    df1 =df1.loc[linhas_trash,:].copy()
    linhas_trash = df1['Road_traffic_density']!= 'NaN '
    df1 =df1.loc[linhas_trash,:].copy()
    linhas_trash = df1['Festival']!= 'NaN '
    df1 =df1.loc[linhas_trash,:].copy()
    
    #Conversões
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    #convertendo de object para float 
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    #convertendo de object para float 
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    
    #convertendo a coluna Order_Date de texto para data 
    
    df1['Order_Date']= pd.to_datetime(df1['Order_Date'],format ='%d-%m-%Y')
    #removendo os espaços 
    df1.loc[:,'ID'] = df1.loc[:,'ID'].str.strip()
    df1.loc[:,'City'] = df1.loc[:,'City'].str.strip()
    df1.loc[:,'Type_of_vehicle'] = df1.loc[:,'Type_of_vehicle'].str.strip()
    df1.loc[:,'Type_of_order'] = df1.loc[:,'Type_of_order'].str.strip()
    df1.loc[:,'Festival'] = df1.loc[:,'Festival'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    
    #Limpando a coluna time_taken 
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min)' )[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)']. astype(int)

    return df1


def order_metric(df1):
    """
    Esta função tem a responsabilidade de mostar o gráfico de linhas pelo número de entregas e a data 
    """
    #colunas
    cols = ['ID','Order_Date']

    #Seleção de colunas
    df_aux =df1.loc[:,cols].groupby('Order_Date').count().reset_index()

    #Desenhar o gráfico de linhas
    fig= px.bar(df_aux, x='Order_Date', y='ID')
    return fig 

def order_by_share(df1):
    df_aux =df1.loc[:,      
    ['ID','Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', : ]
        
    df_aux['entregas_perc'] = df_aux['ID']/df_aux['ID'].sum()
    fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')
    return fig

def order_by_traffic(df1):
    df_aux = df1.loc[:,   ['ID','City','Road_traffic_density']].groupby(['City','Road_traffic_density']).count().reset_index()
                    
    df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN' ,:]

    fig = px.scatter(df_aux, x = 'City', y= 'Road_traffic_density', size='ID', color='City')
    return fig

def order_by_week(df1):
    df1['Week_of_year'] = df1['Order_Date'].dt.strftime( '%U' )
    df_aux01 = df1.loc[:, ['ID','Week_of_year']].groupby('Week_of_year').count().reset_index()
    df_aux02 = df1.loc[: ,    ['Delivery_person_ID','Week_of_year']].groupby('Week_of_year').nunique().reset_index()
    
    df_aux = pd.merge(df_aux01,df_aux02, how='inner')
    
    df_aux['order_by_deliver'] = df_aux['ID']/df_aux['Delivery_person_ID']
              
    fig =px.line(df_aux, x='Week_of_year',y='order_by_deliver')
    return fig  

def share_by_week(df1):
    df_aux01 = df1.loc[:, ['ID','Week_of_year']].groupby('Week_of_year').count().reset_index()
    df_aux02 = df1.loc[: ,['Delivery_person_ID','Week_of_year']].groupby('Week_of_year').nunique().reset_index()

    df_aux = pd.merge(df_aux01,df_aux02, how='inner')

    df_aux['order_by_deliver'] = df_aux['ID']/df_aux['Delivery_person_ID']

    fig= px.line(df_aux, x='Week_of_year',y='order_by_deliver')
    return fig 



def country_maps(df1):
    df_aux = df1.loc[:,['City','Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']].groupby(['City','Road_traffic_density']).median().reset_index()
    df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN' ,:]
        
    map = folium.Map()
        
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],
                       location_info['Delivery_location_longitude']]).add_to(map)
        
    folium_static(map, width=1024, height=600)
# -------------------------------- incio da loógica do código ------------------------------

# import data.set 

df1 = pd.read_csv('train.csv')
#Fazendo um cópia do DataFrame lido 
df1 = df1.copy()
#-------------------------------------
#limpar o código 
#-

df1= clean_code(df1)


#=========================================================================================================
#Barra lateral 
#============================================================================================
st.header('Marketplace - Visão Empresa')

image_path ='food.png'
image = Image.open( image_path)
st.sidebar.image( image, width = 200)

st.sidebar.markdown('# Cury company')
st.sidebar.markdown('## Fastest Delivery in town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
                'Até qual valor?',
                value=datetime(2022,4,6),
                min_value=datetime(2022,2,11),
                max_value=datetime(2022,4,13),
                format='DD-MM-YYYY')

st.sidebar.markdown("""---""")


#traffic_options = st.sidebar.multiselect(
 #       'Quais as condições do trânsito?',
  #      ['Low','Medium', 'High','Jam'],
   #     default=['Low','Medium','High','Jam'])

traffic_options = st.sidebar.multiselect( 
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'], 
    default=['Low', 'Medium', 'High', 'Jam'] )



st.sidebar.markdown("""---""")
st.sidebar.markdown('## Powered by Comunidade DS')
#Filtro de data 
linhas_seleciondas = df1['Order_Date']< date_slider
df1= df1.loc[linhas_seleciondas, :]

#Filtro de trânsito


linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]



#=============================================================================================
#Layout do Streamlit 
#===========================================================================================

tab1,tab2,tab3 = st.tabs(['Visão Gerencial','Visão tática', 'Visão Geográfica'])

with tab1:
    st.markdown('# Orders by day')
    fig = order_metric(df1)
    st.plotly_chart(fig, use_container_width=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.header('Traffic Order Share') 
        fig = order_by_share(df1)
        st.plotly_chart(fig,use_container_width=True)
        
    with col2:
        st.header('Traffic Order City')
        fig = order_by_traffic(df1)
        st.plotly_chart(fig,use_container_width=True)
        
with tab2:
    with st.container():
         st.markdown('# Order by Week')
         fig = order_by_week(df1)
         st.plotly_chart(fig,use_container_width=True)
        
    with st.container():
        st.markdown('# Order Share by Week')
        fig = share_by_week(df1)
        st.plotly_chart(fig,use_container_width=True)
        
with tab3:
    st.markdown('# Country Maps ')
    country_maps (df1)