#bibliotecas:
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from app_variables import *
import basedosdados as bd


@st.cache(allow_output_mutation=True)
def get_data_vac():
    df = bd.read_sql("""SELECT id_paciente, idade_paciente, sexo_paciente, raca_cor_paciente, 
    grupo_atendimento_vacina, categoria_vacina, nome_fabricante_vacina, data_aplicacao_vacina, dose_vacina
    FROM `basedosdados.br_ms_vacinacao_covid19.microdados` 
    WHERE (id_municipio_endereco_paciente = '4205407');""",
                     billing_project_id="vacina-356317",
                     reauth=False)
    return df

def get_data_posto( path_posto ):
    df_posto = pd.read_csv( path_posto, sep=",", encoding="ISO-8859-1" )
    return df_posto

def introd():
    st.markdown('<style>body{background-color: #fbfff0}</style>', unsafe_allow_html=True)
    st.markdown(html_title, unsafe_allow_html=True)
    st.markdown(""" <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)
    return None

def rodape():
    st.markdown(html_rodape, unsafe_allow_html=True)
    return None

def bem_vindo():
    st.markdown("""###""")
    st.markdown(html_card_header_0A_1_11, unsafe_allow_html=True)
    st.markdown(html_card_body_0A_1_11, unsafe_allow_html=True)
    st.markdown("""###""")

    col1, col2, col3, col4 , col5 = st.columns([1, 20, 1, 20, 1])
    with col1:
        st.write("")
    with col2:
        st.markdown(html_card_header_0A_1_21, unsafe_allow_html=True)
        st.markdown(html_card_body_0A_1_21, unsafe_allow_html=True)
    with col3:
        st.write("")
    with col4:
        st.markdown(html_card_header_0A_1_22, unsafe_allow_html=True)
        st.markdown("""""")
        st.markdown(
            """🎲  [Código Aberto no Github](https://github.com/MateusOF5512/TesteHeroku)""")
        st.markdown(
            """🎲   [Dados sobre o CENSO IBGE 2010](https://cidades.ibge.gov.br/brasil/sc/florianopolis/pesquisa/23/24304?indicador=29455)""")
        st.markdown(
            """🎲   [Dados sobre a Campanha de Vacinação Contra Covid-19](https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao)""")

    with col5:
          st.write("")

    return None


def como_usar():
    st.markdown("""---""")
    st.markdown(html_header_02, unsafe_allow_html=True)
    st.markdown("""---""")
    st.markdown(html_subheader_01, unsafe_allow_html=True)
    st.markdown("""###""")

    col1, col2, col3, col4, col5 = st.columns([1, 20, 1, 10, 1])
    with col1:
        st.write("")
    with col2:
        st.markdown(html_card_header_00A_1_11, unsafe_allow_html=True)
        st.markdown(html_card_body_00A_1_11, unsafe_allow_html=True)
    with col3:
        st.write("")
    with col4:
        st.markdown(html_card_header_00A_1_12, unsafe_allow_html=True)
        st.markdown(html_card_body_00A_1_12, unsafe_allow_html=True)

    with col5:
        st.write("")

    st.markdown("""---""")
    st.markdown(html_subheader_02, unsafe_allow_html=True)
    st.markdown("""*Adicionar Texto*""")
    st.markdown("""###""")

    st.markdown("""---""")
    st.markdown(html_subheader_03, unsafe_allow_html=True)
    st.markdown("""*Adicionar Texto*""")

    return None



def teste1(df):
    st.dataframe(data=df, width=550, height=400)

    return None