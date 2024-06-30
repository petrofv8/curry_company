import streamlit as st 
from PIL import Image 

st.set_page_config(
   page_title ='Home')

image_path='food.png'
image = Image.open ('food.png')
st.sidebar.image(image, width = 200)


st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )

st.write(' # Cury company growth dashboard')

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar o crescimmento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial : Métricas gerais de comportamento 
        - Visão Tática : Indicadores semanais de crescimento 
        - Visão Geográfica : Insights de geolocalização. 
    -Visão Entregador :
        - Acompanhamento dos indicadores semanais de crescimento.

    ### Ask for help 
        - Time de Data Science no Discord 
        @petro05560
    """)
