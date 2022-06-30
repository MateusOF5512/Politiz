# 0.1 - Bibliotecas:
#import pandas as pd
#import numpy as np
#import plotly.graph_objects as go
#import folium
import streamlit as st
from Stream_variables import *



def introd():
    st.markdown('<style>body{background-color: #fbfff0}</style>', unsafe_allow_html=True)
    st.markdown(html_title, unsafe_allow_html=True)
    st.markdown(""" <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)
    return None


# 0.5 - Rodapé das paginas
def rodape():
    st.write(html_rodape, unsafe_allow_html=True)
    return None


def atas_modelo():
    st.header("Ata XXX")
    st.markdown("*Instância Deliberativa:* CONSELHO UNIVERSITÁRIO")
    st.markdown("Sessão: 03 de 22.1, em 31/03/2022, às 14h")
    st.subheader("Participantes:")
    with st.container():
        col1A, col2A, col3A, col4A, col5A, col6A, col7A = st.columns([3, 10, 2, 10, 1, 10, 1])
        with col1A:
            st.write("")
        with col2A:
            st.markdown("PROFESSORES:* 03 de 22.1, em 31/03/2022, às 14h")
        with col3A:
            st.write("")
        with col4A:
            st.markdown("PROFESSORES:* 03 de 22.1, em 31/03/2022, às 14h")
        with col5A:
            st.write("")
        with col6A:
            st.markdown("PROFESSORES:* 03 de 22.1, em 31/03/2022, às 14h")
        with col7A:
            st.write("")

    return None

############################################################################################
def bot():

    with st.container():
        col1A, col2A, col3A, col4A, col5A, col6A, col7A = st.columns([3, 10, 2, 10, 1, 10, 1])
        with col1A:
            st.write("")
        with col2A:
            BOT_ATAS = st.button(label="Atas das Instâncias")
        with col3A:
            st.write("")
        with col4A:
            BOT_CALENDARIO = st.button(label="Calendário de Eventos")
        with col5A:
            st.write("")
        with col6A:
            BOT_INFOS = st.button(label="Informações sobre as Instâncias")
        with col7A:
            st.write("")


    if BOT_ATAS:

        st.title("Atas Divididas postância Deiberativa")
        col1A, col2A, col3A, col4A, col5A = st.columns([3, 10, 2, 10, 1])
        with col1A:
            st.write("")
        with col2A:
            st.subheader("Instâncias Institucionais da UFSC:")
            BOT_COLCUR = st.button("Colegiado de Curso")

            if BOT_COLCUR:
                st.header("Ata XXX")
                st.markdown("*Instância Deliberativa:* CONSELHO UNIVERSITÁRIO")
                st.markdown("Sessão: 03 de 22.1, em 31/03/2022, às 14h")
                st.subheader("Participantes:")
                with st.container():
                    col1A, col2A, col3A, col4A, col5A, col6A, col7A = st.columns([3, 10, 2, 10, 1, 10, 1])
                    with col1A:
                        st.write("")
                    with col2A:
                        st.markdown("PROFESSORES:* 03 de 22.1, em 31/03/2022, às 14h")
                    with col3A:
                        st.write("")
                    with col4A:
                        st.markdown("PROFESSORES:* 03 de 22.1, em 31/03/2022, às 14h")
                    with col5A:
                        st.write("")
                    with col6A:
                        st.markdown("PROFESSORES:* 03 de 22.1, em 31/03/2022, às 14h")
                    with col7A:
                        st.write("")
            BOT_COLDEP = st.button(label="Colegiado de Departamento")
            BOT_CONSCETC = st.button(label="Conselho do CTC")
            BOT_CAMGRAD = st.button(label="Câmara de Graduação")
            BOT_CONSUNI = st.button(label="Conselho Universitário")
        with col3A:
            st.write("")
        with col4A:
            st.subheader("Instâncias Estudantis da UFSC")
            BOT_CETEC = st.button(label="CETEC")
            BOT_CEB = st.button(label="CEB")
            BOT_DCE = st.button(label="Diretório Acâdemico - DCE")
            BOT_CEB = st.button(label="Assembléia Geral Estudantil")
        with col5A:
            st.write("")

        if BOT_COLDEP:
            atas_modelo()

        if BOT_CONSCETC:
            atas_modelo()

        if BOT_CAMGRAD:
            atas_modelo()

        if BOT_CONSUNI:
            atas_modelo()

    st.write("ATAS AQUI")

    if BOT_CALENDARIO:
        st.write("CALENDARIO AQUI")

    if BOT_INFOS:
        st.write("INFOS")



    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    return None

