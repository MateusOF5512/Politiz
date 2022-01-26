# 0.1 - Bibliotecas:
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from folium import plugins
from app_variables import *
from app_functions import *

# Configurando aplicação e tratando os dados
st.set_page_config(page_title="Exploração de Dados Abertos", page_icon=":telescope:", layout="wide") # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
df = get_data_vac( path_vac )
df_selection = set_feature( df )


introd()
menu = st.selectbox(label="Selecione Aqui sua Exploração!",
                    options=("Apresentação Inicial",
                         "1 - Descrição da Campanha de Vacinação",
                         "2 - Características da População Vacinada",
                         "3 - Informações dos Postos de Vacinação"))


if menu == 'Apresentação Inicial':
    inicial()
    rodape()

elif menu == '1 - Descrição da Campanha de Vacinação':
    campanha1( df_selection )
    rodape()

elif menu == '2 - Características da População Vacinada':
    caracteristicas2_blocoA( df_selection )
    caracteristicas2_blocoB(df_selection )
    caracteristicas2_blocoC( df_selection )
    rodape()

elif menu == "3 - Informações dos Postos de Vacinação":
    mapas3( df_selection )
    rodape()

else:
    error()
    rodape()