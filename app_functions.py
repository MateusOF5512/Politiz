# 0.1 - Bibliotecas:
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from folium import plugins
from app_variables import *

# 0.2 - Lendo os Dados
@st.cache(allow_output_mutation=True)
def get_data_vac( path_vac ):
    df = pd.read_csv( path_vac, sep=",", encoding="ISO-8859-1" )
    return df

# 0.3 - Criando novas variaveis
def set_feature( df ):
    df["vacina_dataAplicacao"] = pd.to_datetime(df["vacina_dataAplicacao"]).dt.strftime("%Y-%m-%d")
    df.at[358702, "vacina_dataAplicacao"] = "2021-11-08"

    df['1° Dose']      = np.where(df['vacina_descricao_dose'] == '1 Dose', 1, 0)
    df['2° Dose']      = np.where(df['vacina_descricao_dose'] == '2 Dose', 1, 0)
    df['Dose Reforco'] = np.where(df['vacina_descricao_dose'] == 'Dose Reforco', 1, 0)
    df['Dose Única']   = np.where(df['vacina_descricao_dose'] == 'Dose Unica', 1, 0)

    df['AstraZeneca'] = np.where(df['vacina_nome'] == 'Astrazeneca', 1, 0)
    df['Pfizer']      = np.where(df['vacina_nome'] == 'Pfizer', 1, 0)
    df['Coronavac']   = np.where(df['vacina_nome'] == 'Coronavac', 1, 0)
    df['Janssen']     = np.where(df['vacina_nome'] == 'Janssen', 1, 0)

    df['Feminino']  = np.where(df['paciente_enumSexoBiologico'] == 'Feminino', 1, 0)
    df['Masculino'] = np.where(df['paciente_enumSexoBiologico'] == 'Masculino', 1, 0)

    df['BRANCA']         = np.where(df['paciente_racaCor_valor'] == 'BRANCA', 1, 0)
    df['PRETA']          = np.where(df['paciente_racaCor_valor'] == 'PRETA', 1, 0)
    df['PARDA']          = np.where(df['paciente_racaCor_valor'] == 'PARDA', 1, 0)
    df['AMARELA']        = np.where(df['paciente_racaCor_valor'] == 'AMARELA', 1, 0)
    df['INDIGENA']       = np.where(df['paciente_racaCor_valor'] == 'INDIGENA', 1, 0)
    df['SEM INFORMACAO'] = np.where(df['paciente_racaCor_valor'] == 'SEM INFORMACAO', 1, 0)

    conditions = [
        (df['paciente_idade'] <= 19),
        (df['paciente_idade'] >= 20) & (df['paciente_idade'] <= 39),
        (df['paciente_idade'] >= 40) & (df['paciente_idade'] <= 59),
        (df['paciente_idade'] >= 60) & (df['paciente_idade'] <= 79),
        (df['paciente_idade'] >= 80)]
    values = ['menos 19 anos', '20 a 39 anos', '40 a 59 anos', '60 a 79 anos', 'mais 80 anos']
    df['faixa_etaria'] = np.select(conditions, values)

    df['menos 19 anos'] = np.where(df['faixa_etaria'] == 'menos 19 anos', 1, 0)
    df['20 a 39 anos'] = np.where(df['faixa_etaria'] == '20 a 39 anos', 1, 0)
    df['40 a 59 anos'] = np.where(df['faixa_etaria'] == '40 a 59 anos', 1, 0)
    df['60 a 79 anos'] = np.where(df['faixa_etaria'] == '60 a 79 anos', 1, 0)
    df['mais 80 anos'] = np.where(df['faixa_etaria'] == 'mais 80 anos', 1, 0)

    df["Total Doses"] = df["1° Dose"] + df["2° Dose"] + df["Dose Única"] + df["Dose Reforco"]

    df_selection = df

    return df_selection

# 0.4 - Cabeçalho das paginas
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
    st.markdown(html_rodape, unsafe_allow_html=True)

    return None

# 0.6 - Apresentação Inicial
def inicial():
    st.markdown("""###""")
    st.markdown(html_card_header_0A_1_11, unsafe_allow_html=True) # Descrição dos Dados</h4>
    st.markdown(html_card_body_0A_1_11, unsafe_allow_html=True)   # ...Dados do CENSO de 2010 (mais recente).</h8>
    st.markdown("""###""")

    return None

def error():
    st.markdown("""###""")
    st.markdown("""Erro: Escolha outra pagina""")
    st.markdown("""###""")

    return None

# 1. 1 - Descrição da Campanha de Vacinação</h2>
def campanha1( df_selection ):
    st.markdown("""---""")
    st.markdown(html_header_01, unsafe_allow_html=True) # 1 - Descrição da Campanha de Vacinação</h2>
    st.markdown("""---""")
    st.markdown(html_subheader_11, unsafe_allow_html=True) # >1.1 - Número de Doses & Vacinas Aplicadas</h3>
    st.markdown("""###""")

# 1.1 - 1 : Declaração de variáveis e Pré-Plot - Geral
    popul_residente = int(421240) #População de Florianópolis
    imun_rebanho = int(326992)    #Imunidade de rebanho(80% da população)
    vacinados_1dose = int(df_selection['1° Dose'].sum()) # Total de Vacinados com 1° Dose
    vacinados_completo = int(df_selection['2° Dose'].sum() + df_selection['Dose Única'].sum())# Total de Vacinados com 2° Dose ou Dose Única

    pop_sem_1dose = (popul_residente - vacinados_1dose)    #Total da população sem 1°dose (pizza)
    pop_sem_2dose = (popul_residente - vacinados_completo) #Total da população sem 2° dose ou unica (pizza)

    with st.container():
        col1A, col2A, col3A, col4A, col5A, col6A, col7A, col8A, col9A = st.columns([1, 15, 1, 15, 1, 15, 1, 15, 1])
        with col1A:
            st.write("")
        with col2A:
            # 1.1 - 1.1 : Declaração de variáveis e Pré-Plot - Pizza 01
            labels2 = ['População com 1° Dose', "População sem 1° Dose:"]
            colors2 = ['#4169E1', '#b3b3b3']

            # 1.1 - 1:1 : Plotagem da Visualização - Pizza 01
            fig1 = go.Figure(data=[go.Pie(labels=labels2,
                                          values=[vacinados_1dose, pop_sem_1dose],
                                          textinfo='percent',
                                          showlegend=False,
                                          marker=dict(colors=colors2,
                                                      line=dict(color='#000010', width=2)))])
            fig1.update_traces(hole=.4, hoverinfo="label+percent+value")
            fig1.update_layout(autosize=False,
                               width=275, height=150, margin=dict(l=20, r=20, b=20, t=30),
                               paper_bgcolor="#f0f0ff", font={'size': 20})

            st.markdown(html_card_header_1A1, unsafe_allow_html=True)  # Vacinados com 1° Dose: Proporção</h5>
            st.plotly_chart(fig1)                                      # 1.1 - 1.1 : Gráfico de Pizza 01
        with col3A:
            st.write("")
        with col4A:
            # 1.1 - 1:2 : Plotagem da Visualização - Velocimtro 01
            fig2 = go.Figure()
            fig2.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=vacinados_1dose,
                domain={'x': [0, 1], 'y': [0, 1]},
                delta={'reference': popul_residente, 'decreasing': {'color': "Red"}},
                gauge={
                    'axis': {'range': [0, popul_residente], 'tickwidth': 2, 'tickcolor': "#0d0d0d"},
                    'bordercolor': "#0d0d0d",
                    'bar': {'color': "#4169E1"},
                    'bgcolor': "#b3b3b3",
                    'borderwidth': 1.5,
                    'steps': [
                        {'range': [0, vacinados_1dose], 'color': "#ADD8E6"}],
                    'threshold': {
                        'line': {'color': "Red", 'width': 10},
                        'thickness': 1,
                        'value': popul_residente}}))
            fig2.update_layout(autosize=False,
                               width=275, height=150, margin=dict(l=20, r=20, b=20, t=30),
                               paper_bgcolor="#f0f0ff", font={'size': 20})

            st.markdown(html_card_header_1A2, unsafe_allow_html=True)  # Vacinados com 1° Dose: Quantidade</h5>
            st.plotly_chart(fig2)                                      # 1.1 - 1.2: Gráfico Velocimetro 01
        with col5A:
            st.write("")
        with col6A:
            # 1.1 - 1:3 : Plotagem da Visualização - Velocimtro 02
            fig3 = go.Figure()
            fig3.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=vacinados_completo,
                domain={'x': [0, 1], 'y': [0, 1]},
                delta={'reference': popul_residente, 'increasing': {'color': "Green"}},
                gauge={
                    'axis': {'range': [0, popul_residente], 'tickwidth': 2, 'tickcolor': "#0d0d0d"},
                    'bordercolor': "#0d0d0d",
                    'bar': {'color': "#D70270"},
                    'bgcolor': "#b3b3b3",
                    'borderwidth': 1.5,
                    'steps': [
                        {'range': [0, vacinados_completo], 'color': "#FFC0CB"}],
                    'threshold': {
                        'line': {'color': "red", 'width': 10},
                        'thickness': 1,
                        'value': popul_residente}}))
            fig3.update_layout(autosize=False,
                               width=275, height=150, margin=dict(l=20, r=20, b=20, t=30),
                               paper_bgcolor="#f0f0ff", font={'size': 20})

            st.markdown(html_card_header_1A3, unsafe_allow_html=True)  # Vacinados Completamente: Quantidade</h5>
            st.plotly_chart(fig3)                                      # 1.1 - 1.3: Gráfico Velocimetro 02
        with col7A:
            st.write("")
        with col8A:
            # 1.1 - 1.4 : Declaração de variáveis e Pré-Plot - Pizza 02
            labels3 = ['Vacinados Completamente', 'Vacinados Incompletamente']
            colors3 = ['#D70270', '#b3b3b3']

            # 1.1 - 1:4 : Plotagem da Visualização - Pizza 01
            fig4 = go.Figure(data=[go.Pie(labels=labels3,
                                          values=[vacinados_completo, pop_sem_2dose],
                                          textinfo='percent', textfont_size=20,
                                          showlegend=False,
                                          marker=dict(colors=colors3,
                                                      line=dict(color=' #000010', width=2)))])
            fig4.update_traces(hole=.4, hoverinfo="label+percent+value")
            fig4.update_layout(autosize=False,
                               width=275, height=150, margin=dict(l=20, r=20, b=20, t=30),
                               paper_bgcolor="#f0f0ff", font={'size': 20})

            st.markdown(html_card_header_1A4, unsafe_allow_html=True)  # Vacinados Completamente: Proporção</h5>
            st.plotly_chart(fig4)                                      # 1.1 - 1.4: Gráfico de Pizza 02
        with col9A:
            st.write("")

    with st.container():
        col1B, col2B, col3B, col4B, col5B = st.columns([1, 20, 1, 20, 1, ])
        with col1B:
            st.write("")
        with col2B:
            # 1.1 - 2.1 : Declaração de variáveis e Pré-Plot - Barra 01
            df = df_selection.groupby(['vacina_descricao_dose']).sum().reset_index()

            values = ['1 Dose', '2 Dose', 'Dose Reforco', 'Dose Unica']
            y_Pfizer = [df['Pfizer'][0], df['Pfizer'][1], df['Pfizer'][2], df['Pfizer'][3]]
            y_AstraZeneca = [df['AstraZeneca'][0], df['AstraZeneca'][1], df['AstraZeneca'][2], df['AstraZeneca'][3]]
            y_Coronavac = [df['Coronavac'][0], df['Coronavac'][1], df['Coronavac'][2], df['Coronavac'][3]]
            y_Janssen = [df['Janssen'][0], df['Janssen'][1], df['Janssen'][2], df['Janssen'][3]]

            # 1.1 - 2:1 : Plotagem da Visualização - Barra 01
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(name='Pfizer', x=values, y=y_Pfizer,
                                  text=y_Pfizer, textposition='auto',
                                  marker_color='#D70270', marker_line_color="#0d0d0d", marker_line_width=1.5))
            fig1.add_trace(go.Bar(name='AstraZeneca', x=values, y=y_AstraZeneca,
                                  text=y_AstraZeneca, textposition='auto',
                                  marker_color='#4169E1', marker_line_color="#0d0d0d", marker_line_width=1.5))
            fig1.add_trace(go.Bar(name='Coronavac', x=values, y=y_Coronavac,
                                  text=y_Coronavac, textposition='auto',
                                  marker_color='#8A2BE2', marker_line_color="#0d0d0d", marker_line_width=1.5))
            fig1.add_trace(go.Bar(name='Janssen', x=values, y=y_Janssen,
                                  text=y_Janssen, textposition='outside',
                                  marker_color='#00cccc', marker_line_color="#0d0d0d", marker_line_width=1.5))
            fig1.update_layout(legend_font_size=12, autosize=False,
                               paper_bgcolor="#f0f0ff", plot_bgcolor="#f0f0ff",
                               font={'color': "#0d0d0d", 'family': "sans-serif"}, height=250, width=550,
                               margin=dict(l=2, r=2, b=4, t=4),
                               legend_bordercolor="#0d0d0d", legend_borderwidth=0.5,
                               legend=dict(orientation="v",
                                           yanchor="top",
                                           y=0.99,
                                           xanchor="right",
                                           x=0.99),
                               barmode='group',
                               bargap=0.2,
                               bargroupgap=0.15 )
            fig1.update_xaxes(
                title_text='Doses Aplicadas',
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9))
            fig1.update_yaxes(
                title_text="Número de Vacinados",
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                nticks=8, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

            st.markdown(html_card_header_1B11, unsafe_allow_html=True)  # Vacinados Completamente: Proporção</h5>
            st.plotly_chart(fig1)                                       # Grágivo de Barra 01

            # 1.1 - 2.2 : Declaração de variáveis e Pré-Plot - Funil 01
            y_Pfizer = int(df_selection['Pfizer'].sum())
            y_AstraZeneca = int(df_selection['AstraZeneca'].sum())
            y_Coronavac = int(df_selection['Coronavac'].sum())
            y_Janssen = int(df_selection['Janssen'].sum())
            y = [y_Pfizer, y_AstraZeneca, y_Coronavac, y_Janssen]
            values = [ "Pfizer", "AstraZeneca", "Coronavac", "Janssen"]

            # 1.1 - 2:2 : Plotagem da Visualização - Funil 01
            fig2 = go.Figure()
            fig2.add_trace(go.Funnel(
                y=values, x=y,
                textposition="inside",
                textinfo="value+percent total",
                opacity=1, marker={"color": ["#D70270", "#4169E1", "#8A2BE2", "#00cccc"],
                                   "line": {"width": [1.5, 1.5, 1.5, 1.5, 1.5],
                                            "color": ["#0d0d0d", "#0d0d0d", "#0d0d0d", "#0d0d0d"]}},
                connector={"line": {"color": "#0d0d0d", "dash": "solid", "width": 1}}))
            fig2.update_layout(paper_bgcolor="#f0f0ff", plot_bgcolor="#f0f0ff",
                               font={'color': "#0d0d0d", 'family': "sans-serif"}, height=200, width=550,
                               margin=dict(l=2, r=2, b=4, t=4))

            st.markdown(html_card_header_1B12, unsafe_allow_html=True)  # Proporção entre as Vacinas Aplicadas</h5>
            st.plotly_chart(fig2)                                       # Gráfico de Funil 01
    with col3B:
        st.write("")
    with col4B:
        # 1.1 - 2.3 : Declaração de variáveis e Pré-Plot - Tabela 01
        df_new = df_selection.groupby(['paciente_id']).sum().reset_index()
        df_new = df_new[["paciente_id", "Total Doses",
                         "1° Dose", "2° Dose", "Dose Única", "Dose Reforco"
                         ]]
        # 1.1 - 2:3 : Plotagem da Visualização - Tabela 01
        st.markdown(html_card_header_1B2, unsafe_allow_html=True)  # Vacinados Completamente: Proporção</h5>
        st.dataframe(data=df_new, width=560, height=515)           # Tabela 01
    with col5B:
        st.write("")

# 1.2 - Variação das Doses & Vacinas Aplicadas</h3> -------------------------------------------------------------------------
    st.markdown("""---""")
    st.markdown(html_subheader_12, unsafe_allow_html=True) #1.2 - Variação das Doses & Vacinas Aplicadas</h3>
    st.markdown("""###""")

    with st.container():
        col1B, col2B, col3B, col4B, col5B = st.columns([1, 20, 1, 20, 1, ])
        with col1B:
            st.write("")
        with col2B:
            # 1.2 - 1.1 : Declaração de variáveis e Pré-Plot - Linha 01
            df_area = df_selection.groupby(['vacina_dataAplicacao']).sum().reset_index()

            # 1.2 - 1:1 : Plotagem da Visualização - Linha 01
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['1° Dose'],
                name='1° Dose',
                mode='lines',
                line=dict(width=1, color='#4169E1'),
                stackgroup='one'))
            fig1.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['2° Dose'],
                name='2° Dose',
                mode='lines',
                line=dict(width=1, color='#D70270'),
                stackgroup='two'))
            fig1.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['Dose Única'],
                name='Dose Única',
                mode='lines',
                line=dict(width=1, color='#00cccc'),
                stackgroup='three'))
            fig1.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['Dose Reforco'],
                name='Dose Reforco',
                mode='lines',
                line=dict(width=1, color='#8A2BE2'),
                stackgroup='four'))
            fig1.update_layout(legend_font_size=10,
                               paper_bgcolor="#f0f0ff", plot_bgcolor="#f0f0ff",
                               font={'color': "#0d0d0d", 'family': "sans-serif"}, height=250, width=550,
                               margin=dict(l=10, r=10, b=10, t=10),
                               legend=dict(bordercolor="#0d0d0d",
                                           borderwidth=0.5,
                                           orientation="v",
                                           yanchor="top",
                                           y=0.98,
                                           xanchor="right",
                                           x=0.98))
            fig1.update_xaxes(
                title_text='Dias da Aplicação da Vacina',
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                rangeslider_visible=True, showgrid=False)
            fig1.update_yaxes(
                title_text="Número de Vacinados",
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

            st.markdown(html_card_header_1C11, unsafe_allow_html=True)  # Variação das Doses Aplicadas</h5>
            st.plotly_chart(fig1)                                       # Gráfico de Linha com Area 01

            # 1.2 - 1.2 : Declaração de variáveis e Pré-Plot - Linha 02
            df_area = df_selection.groupby(['vacina_dataAplicacao']).sum().reset_index()

            # 1.2 - 1:2 : Plotagem da Visualização - Linha 02
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['AstraZeneca'],
                name='AstraZeneca',
                mode='lines',
                line=dict(width=1, color='#D70270'),
                stackgroup='one'))
            fig2.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['Pfizer'],
                name='Pfizer',
                mode='lines',
                line=dict(width=1, color='#4169E1'),
                stackgroup='two'))
            fig2.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['Coronavac'],
                name='Coronavac',
                mode='lines',
                line=dict(width=1, color='#8A2BE2'),
                stackgroup='four'))
            fig2.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['Janssen'],
                name='Janssen',
                mode='lines',
                line=dict(width=1, color='#00cccc'),
                stackgroup='five'))
            fig2.update_layout(paper_bgcolor="#f0f0ff", plot_bgcolor="#f0f0ff",
                               font={'color': "#0d0d0d", 'family': "sans-serif"}, height=250, width=550,
                               margin=dict(l=10, r=10, b=10, t=10 ),
                               legend=dict(bordercolor="#0d0d0d", borderwidth=0.5,
                                           font_size=10, orientation="v",
                                           yanchor="top", y=0.98,
                                           xanchor="right", x=0.98))
            fig2.update_xaxes(
                title_text='Dia da Aplicação da Vacina',
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                rangeslider_visible=True, showgrid=False)
            fig2.update_yaxes(
                title_text="Número de Vacinados",
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

            st.markdown(html_card_header_1C12, unsafe_allow_html=True)  # Variação das Vacinas Aplicadas</h5>
            st.plotly_chart(fig2)                                       # Gráfico de Linha com Area 02

        with col3B:
            st.write("")
        with col4B:
            # 1.2 - 1.3 : Declaração de variáveis e Pré-Plot - Tabela 01
            df_filter1 = df_selection[["vacina_dataAplicacao", "Total Doses",
                                       "1° Dose", "2° Dose", "Dose Única", "Dose Reforco",
                                       "AstraZeneca", "Pfizer", "Coronavac", "Janssen",
                                       ]]
            df_new1 = df_filter1.groupby('vacina_dataAplicacao').sum().reset_index()

            # 1.2 - 1:3 : Plotagem da Visualização - Tabela 01
            st.markdown(html_card_header_1C20, unsafe_allow_html=True) #
            st.dataframe(data=df_new1, width=560, height=560)          #
        with col5B:
            st.write("")

    return None

# 2 - Características da População Vacinada
def caracteristicas2_blocoA( df_selection ):
    st.markdown("""---""")
    st.markdown(html_header_20, unsafe_allow_html=True)        # 2 - Características da População Vacinada
    st.markdown("""---""")
    st.markdown(html_subheader_2A_10, unsafe_allow_html=True)  # 2.1 - Sexo Biológico
    st.markdown("""###""")

    with st.container():
        col1A, col2A, col3A, col4A, col5A, col6A, col7A = st.columns([1, 15, 1, 15, 1, 15, 1])
        with col1A:
            st.write("")
        with col2A:
            # 2.1 - 1. : Declaração de variáveis e Pré-Plot - Geral
            df_selection1 = df_selection.drop_duplicates(subset=['paciente_id'], keep="last")

            popul_femi = int(218193)
            popul_masc = int(203047)
            vacinados_femi = int(df_selection1['Feminino'].sum())
            vacinados_masc = int(df_selection1['Masculino'].sum())

            # 2.1 - 1:1 : Plotagem da Visualização - Velocimetro 03
            fig1 = go.Figure()
            fig1.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=vacinados_masc,
                domain={'x': [0, 1], 'y': [0, 1]},
                delta={'reference': popul_masc, 'increasing': {'color': "Green"}},
                gauge={
                    'axis': {'range': [0, popul_masc], 'tickwidth': 2, 'tickcolor': "#0d0d0d"},
                    'bordercolor': "#0d0d0d",
                    'bar': {'color': "#4169E1"},
                    'bgcolor': "#b3b3b3",
                    'borderwidth': 1.5,
                    'steps': [
                        {'range': [0, vacinados_masc], 'color': "#ADD8E6"}],
                    'threshold': {
                        'line': {'color': "red", 'width':8},
                        'thickness': 1,
                        'value': popul_masc}}))
            fig1.update_layout(autosize=False,
                               width=360, height=150, margin=dict(l=20, r=20, b=20, t=30),
                               paper_bgcolor="#f0f0ff", font={'size': 20})

            st.markdown(html_card_header_2A_1_11, unsafe_allow_html=True) #>Vacinados do Sexo Masculino</h5>
            st.plotly_chart(fig1, use_container_width=True)               # Gráfico de Velocimtro 03
        with col3A:
            st.write("")
        with col4A:
            # 2.1 - 1.2 : Declaração de variáveis e Pré-Plot - Pizza 03
            labels1 = ['Sexo Feminino', 'Sexo Masculino']
            colors1 = ['#D70270', '#4169E1']  # magenta | royalblue

            # 2.1 - 1:2 : Plotagem da Visualização - Pizza 03
            fig2 = go.Figure(data=[go.Pie(labels=labels1,
                                          values=[vacinados_femi, vacinados_masc],
                                          textinfo='percent', textfont_size=20,
                                          showlegend=False,
                                          marker=dict(colors=colors1,
                                                      line=dict(color='black', width=2)))])
            fig2.update_traces(hole=.4, hoverinfo="label+percent+value")
            fig2.update_layout(autosize=False,
                               width=360, height=150, margin=dict(l=20, r=20, b=20, t=30),
                               paper_bgcolor="#f0f0ff", font={'size': 20})

            st.markdown(html_card_header_2A_1_12, unsafe_allow_html=True) #>Proporção entre os Sexos</h5>
            st.plotly_chart(fig2, use_container_width=True)               # Gráfico de Pizza 03
        with col5A:
            st.write("")
        with col6A:
            # 2.1 - 1:3 : Plotagem da Visualização - Velocimetro 04
            fig3 = go.Figure()
            fig3.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=vacinados_femi,
                domain={'x': [0, 1], 'y': [0, 1]},
                delta={'reference': popul_femi, 'increasing': {'color': "Green"}},
                gauge={
                    'axis': {'range': [0, popul_femi], 'tickwidth': 2, 'tickcolor': "#0d0d0d"},
                    'bordercolor': "#0d0d0d",
                    'bar': {'color': "#D70270"},
                    'bgcolor': "#b3b3b3",
                    'borderwidth': 1.5,
                    'steps': [
                        {'range': [0, vacinados_femi], 'color': "#FFC0CB"}],
                    'threshold': {
                        'line': {'color': "Green", 'width': 8},
                        'thickness': 1,
                        'value': popul_femi}}))
            fig3.update_layout(autosize=False,
                               width=360, height=150, margin=dict(l=20, r=20, b=20, t=30),
                               paper_bgcolor="#f0f0ff", font={'size': 20})

            st.markdown(html_card_header_2A_1_13, unsafe_allow_html=True)  #>Vacinados do Sexo Feminino</h5>
            st.plotly_chart(fig3, use_container_width=True)                # Gráfico de Velocimetro 04
        with col7A:
            st.write("")


    with st.container():
        col1B, col2B, col3B = st.columns([1, 25, 1])
        with col1B:
            st.write("")
        with col2B:
            # 2.1 - 2.1 : Declaração de variáveis e Pré-Plot - Tabela 04
            df_new = df_selection.groupby(['paciente_enumSexoBiologico']).sum().reset_index()
            df_new = df_new[["paciente_enumSexoBiologico", "Total Doses",
                             "1° Dose", "2° Dose", "Dose Única", "Dose Reforco",
                             "AstraZeneca", "Pfizer", "Coronavac", "Janssen"]]

            # 2.1 - 2:1 : Plotagem da Visualização - Tabela 04
            st.markdown(html_card_header_2A_1_20, unsafe_allow_html=True)  #>Dados Agrupados por Sexo Biológico</h5>
            st.dataframe(data=df_new, width=1100, height=400)              # Tabela 04
        with col3B:
            st.write("")

    with st.container():
        col1B, col2B, col3B, col4B, col5B = st.columns([1, 20, 1, 20, 1, ])
        with col1B:
            st.write("")
        with col2B:
            # 2.1 - 3.1 : Declaração de variáveis e Pré-Plot - Linha 03
            df_area = df_selection.groupby(['vacina_dataAplicacao']).sum().reset_index()

            # 2.1 - 3:1 : Plotagem da Visualização - Linha 03
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['Masculino'],
                name='Masculino',
                mode='lines',
                line=dict(width=1, color='#4169E1')))
            fig1.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['Feminino'],
                name='Feminino',
                mode='lines',
                line=dict(width=1, color='#D70270')))
            fig1.update_layout(legend_font_size=12, autosize=False,
                               paper_bgcolor="#f0f0ff", plot_bgcolor="#f0f0ff",
                               font={'color': "#0d0d0d", 'family': "sans-serif"}, height=225, width=550,
                               margin=dict(l=10, r=10, b=10, t=10),
                               legend=dict(bordercolor="#0d0d0d", borderwidth=0.5,
                                           orientation="h",
                                           yanchor="top",
                                           y=0.98,
                                           xanchor="left",
                                           x=0.02))
            fig1.update_xaxes(
                title_text='Dias da Aplicação da Vacina',
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                rangeslider_visible=True, showgrid=False)
            fig1.update_yaxes(
                title_text="Número de Vacinados",
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

            st.markdown(html_card_header_2A_1_31, unsafe_allow_html=True)  #>Variação diária de Vacinados</h5>
            st.plotly_chart(fig1)                                          # Gráfico de Linha 03
        with col3B:
            st.write("")
        with col4B:
            # 2.1 - 3.2 : Declaração de variáveis e Pré-Plot - Barra 02
            df = df_selection.groupby(['paciente_enumSexoBiologico']).sum().reset_index()
            values = ['Feminino', 'Masculino']
            y_1dose = [df['1° Dose'][0], df['1° Dose'][1]]
            y_2dose = [df['2° Dose'][0], df['2° Dose'][1]]
            y_Adose = [df['Dose Reforco'][0], df['Dose Reforco'][1]]
            y_Udose = [df['Dose Única'][0], df['Dose Única'][1]]

            # 2.1 - 3:2 : Plotagem da Visualização - Barra 02
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(name='1° Dose', x=values, y=y_1dose,
                                  text=y_1dose, textposition='auto',
                                  marker_color='#4169E1', marker_line_color="#0d0d0d", marker_line_width=1.5))
            fig2.add_trace(go.Bar(name='2° Dose', x=values, y=y_2dose,
                                  text=y_2dose, textposition='auto',
                                  marker_color='#D70270', marker_line_color="#0d0d0d", marker_line_width=1.5))
            fig2.add_trace(go.Bar(name='Dose Única', x=values, y=y_Udose,
                                  text=y_Udose, textposition='auto',
                                  marker_color='#4B0082', marker_line_color="#0d0d0d", marker_line_width=1.5))
            fig2.add_trace(go.Bar(name='Dose Reforco', x=values, y=y_Adose,
                                  text=y_Adose, textposition='auto',
                                  marker_color='#00cccc', marker_line_color="#0d0d0d", marker_line_width=1.5))
            fig2.update_layout(legend_font_size=10, autosize=False,
                               paper_bgcolor="#f0f0ff", plot_bgcolor="#f0f0ff",
                               font={'color': "#0d0d0d", 'family': "sans-serif"}, height=230, width=550,
                               margin=dict(l=10, r=10, b=10, t=10),
                               legend=dict(bordercolor="#0d0d0d", borderwidth=0.5,
                                           orientation="v",
                                           yanchor="top",
                                           y=0.98,
                                           xanchor="right",
                                           x=1),
                               barmode='group')
            fig2.update_xaxes(
                title_text='Sexo  Biológico',
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9))
            fig2.update_yaxes(
                title_text="Doses  Aplicadas",
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

            st.markdown(html_card_header_2A_1_32, unsafe_allow_html=True)  #>Campanha de Vacinação - Doses Aplicadas</h5>
            st.plotly_chart(fig2)                                          # Gráfico de Barra 02
        with col5B:
            st.write("")
    st.markdown("""---""")

    return None

# 2.2 - Raça & Cor ---------------------------------------------------------------------------------------------------------------
def caracteristicas2_blocoB( df_selection ):
    st.markdown(html_subheader_2B_10, unsafe_allow_html=True) # >2.2 - Raça & Cor</h3>
    st.markdown("""###""")

    with st.container():
        col1A, col2A, col3A, col4A, col5A = st.columns([1, 20, 1, 20, 1])
        with col1A:
            st.write("")
        with col2A:
            # 2.2 - 1.1 : Declaração de variáveis e Pré-Plot - Barra 03
            dados = df_selection.drop_duplicates(subset=['paciente_id'], keep="last")

            popul_branca = int(356142)
            popul_parda = int(41009)
            popul_preta = int(20839)
            popul_amarela = int(2196)
            popul_indigena = int(1028)
            popul_semdecl = int(26)
            vacinados_branca = int(dados['BRANCA'].sum())
            vacinados_parda = int(dados['PARDA'].sum())
            vacinados_preta = int(dados['PRETA'].sum())
            vacinados_amarela = int(dados['AMARELA'].sum())
            vacinados_indigena = int(dados['INDIGENA'].sum())
            vacinados_seminfo = int(dados['SEM INFORMACAO'].sum())

            raca_vacina = ['Branca', 'Parda', 'Preta', 'Amarela', 'Indigena', 'Sem Informação']

            y_popul = [popul_branca, popul_preta, popul_parda, popul_amarela, popul_indigena, popul_semdecl]
            y_vacina = [vacinados_branca, vacinados_preta, vacinados_parda, vacinados_amarela, vacinados_indigena, vacinados_seminfo]

            # 2.2 - 1:1 : Plotagem da Visualização - Barra 03
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(name='População Total (2010)', x=raca_vacina, y=y_popul,
                                  text=y_popul, textposition='auto',
                                  marker_color='#4169E1', marker_line_color="#0d0d0d", marker_line_width=1))
            fig1.add_trace(go.Bar(name='População Vacinada', x=raca_vacina, y=y_vacina,
                                  text=y_vacina, textposition='auto',
                                  marker_color='#D70270', marker_line_color="#0d0d0d", marker_line_width=1))
            fig1.update_layout(legend_font_size=10, autosize=False,
                               paper_bgcolor="#f0f0ff", plot_bgcolor="#f0f0ff",
                               font={'color': "#0d0d0d", 'family': "sans-serif"}, height=200, width=550,
                               margin=dict(l=5, r=5, b=5, t=5),
                               legend=dict(bordercolor="#0d0d0d", borderwidth=0.5,
                                           orientation="v",
                                           yanchor="top",
                                           y=0.98,
                                           xanchor="right",
                                           x=0.98),
                               barmode='group')
            fig1.update_xaxes(
                title_text='Raça & Cor',
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9))
            fig1.update_yaxes(
                title_text="População",
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

            st.markdown(html_card_header_2B_2_11, unsafe_allow_html=True)  #  >População Total x População Vacinada</h5>
            st.plotly_chart(fig1, use_container_width=True)                # Gráfico de Barra 03
        with col3A:
            st.write("")
        with col4A:
            # 2.2 - 1.2 : Declaração de variáveis e Pré-Plot - Tabela 03
            df_new = df_selection.groupby(['paciente_racaCor_valor']).sum().reset_index()
            df_new = df_new[["paciente_racaCor_valor", "Total Doses",
                             "1° Dose", "2° Dose", "Dose Única", "Dose Reforco",
                             "AstraZeneca", "Pfizer", "Coronavac", "Janssen"]]

            # 2.2 - 1:2 : Plotagem da Visualização - Tabela 03
            st.markdown(html_card_header_2B_2_12, unsafe_allow_html=True)  #>Dados Agrupados por Raça & Cor</h5>
            st.dataframe(data=df_new, width=550, height=250)               # Tabela 03
        with col5A:
            st.write("")

    with st.container():
        col1B, col2B, col3B, col4B, col5B = st.columns([1, 20, 1, 20, 1])
        with col1B:
            st.write("")
        with col2B:
            # 2.2 - 2.1 : Declaração de variáveis e Pré-Plot - Barra 04
            df = df_selection.groupby(['paciente_racaCor_valor']).sum().reset_index()

            values = ['BRANCA', 'SEM INFORMACAO', 'PRETA', 'PARDA', 'AMARELA', 'INDIGENA']
            y_1dose = [df['1° Dose'][1], df['1° Dose'][5], df['1° Dose'][4], df['1° Dose'][3], df['1° Dose'][0], df['1° Dose'][2]]
            y_2dose = [df['2° Dose'][1], df['2° Dose'][5], df['2° Dose'][4], df['2° Dose'][3], df['2° Dose'][0], df['2° Dose'][2]]
            y_Adose = [df['Dose Reforco'][1], df['Dose Reforco'][5], df['Dose Reforco'][4], df['Dose Reforco'][3], df['Dose Reforco'][0], df['Dose Reforco'][2]]
            y_Udose = [df['Dose Única'][1], df['Dose Única'][5], df['Dose Única'][4], df['Dose Única'][3], df['Dose Única'][0], df['Dose Única'][2]]

            # 2.2 - 2:1 : Plotagem da Visualização - Barra 04
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(name='1° Dose', x=values, y=y_1dose,
                                  text=y_1dose, textposition='auto',
                                  marker_color='#4169E1', marker_line_color="#0d0d0d", marker_line_width=1.5))
            fig1.add_trace(go.Bar(name='2° Dose', x=values, y=y_2dose,
                                  text=y_2dose, textposition='auto',
                                  marker_color='#D70270', marker_line_color="#0d0d0d", marker_line_width=1.5))
            fig1.add_trace(go.Bar(name='Dose Reforco', x=values, y=y_Adose,
                                  text=y_Adose, textposition='auto',
                                  marker_color='#00cccc', marker_line_color="#0d0d0d", marker_line_width=1.5))
            fig1.add_trace(go.Bar(name='Dose Única', x=values, y=y_Udose,
                                  text=y_Udose, textposition='auto',
                                  marker_color='#4B0082', marker_line_color="#0d0d0d", marker_line_width=1.5))
            fig1.update_layout(legend_font_size=10, autosize=False,
                               paper_bgcolor="#f0f0ff", plot_bgcolor="#f0f0ff",
                               font={'color': "#0d0d0d", 'family': "sans-serif"}, height=250, width=550,
                               margin=dict(l=5, r=5, b=5, t=5),
                               legend=dict(bordercolor="#0d0d0d", borderwidth=0.5,
                                           orientation="v",
                                           yanchor="top",
                                           y=0.95,
                                           xanchor="right",
                                           x=0.98),
                               barmode='group')
            fig1.update_xaxes(
                title_text='Sexo Biológico',
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9))
            fig1.update_yaxes(
                title_text="Doses Aplicadas",
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                nticks=8, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

            st.markdown(html_card_header_2B_2_21, unsafe_allow_html=True)  #>Campanha de Vacinação - Doses Aplicadas</h5>
            st.plotly_chart(fig1, use_container_width=True)                # Gráfico de Barra 04
        with col3B:
            st.write("")
        with col4B:
            # 2.2 - 2.2 : Declaração de variáveis e Pré-Plot - Linha 04
            df_area = df_selection.groupby(['vacina_dataAplicacao']).sum().reset_index()

            # 2.2 - 2:2 : Plotagem da Visualização - Linha 04
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['BRANCA'],
                name='BRANCA',
                mode='lines',
                line=dict(width=1, color='#4169E1')))
            fig2.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['SEM INFORMACAO'],
                name='SEM INFORMACAO',
                mode='lines',
                line=dict(width=1, color='#D70270')))
            fig2.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['PRETA'],
                name='PRETA',
                mode='lines',
                line=dict(width=1, color='#00b3b3')))
            fig2.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['PARDA'],
                name='PARDA',
                mode='lines',
                line=dict(width=1, color='#b35900')))
            fig2.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['AMARELA'],
                name='AMARELA',
                mode='lines',
                line=dict(width=1, color='#59b300')))
            fig2.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['INDIGENA'],
                name='INDIGENA',
                mode='lines',
                line=dict(width=1, color='#b30000')))
            fig2.update_layout(legend_font_size=8,
                               paper_bgcolor="#f0f0ff", plot_bgcolor="#f0f0ff",
                               font={'color': "#0d0d0d", 'family': "sans-serif"}, height=250, width=550,
                               margin=dict(l=15, r=5, b=5, t=10),
                               legend=dict(bordercolor="#0d0d0d", borderwidth=0.5,
                                           orientation="v",
                                           yanchor="top",
                                           y=1.15,
                                           xanchor="left",
                                           x=0.01))
            fig2.update_xaxes(
                title_text='Dias da Aplicação da Vacina',
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                rangeslider_visible=True, showgrid=False)
            fig2.update_yaxes(
                title_text="Número de Vacinados",
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                nticks=8, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

            st.markdown(html_card_header_2B_2_22, unsafe_allow_html=True)  # >Variação diária de Vacinados</h5>
            st.plotly_chart(fig2)                                          # Gráfico de Linha 04
        with col5B:
            st.write("")
        st.markdown("""---""")

    return None

# 2.3 - Faixa Etária -----------------------------------------------------------------------------------------------------------------
def caracteristicas2_blocoC( df_selection ):
    st.markdown(html_subheader_2B_30, unsafe_allow_html=True)  #>2.3 - Faixa Etária</h3>
    st.markdown("""###""")

    with st.container():
        col1A, col2A, col3A, col4A, col5A = st.columns([1, 20, 1, 20, 1])
        with col1A:
            st.write("")
        with col2A:
            # 2.3 - 1.1 : Declaração de variáveis e Pré-Plot - Barra 05
            dados1 = df_selection.drop_duplicates(subset=['paciente_id'], keep="last")
            df = dados1.groupby(['faixa_etaria']).sum().reset_index()

            values = ['menos 19 anos', '20 a 39 anos', '40 a 59 anos', '60 a 79 anos', 'mais 80 anos']
            y_pop = [107978, 155814, 109025, 41639, 6784]
            y_vac = [df['menos 19 anos'][4], df['20 a 39 anos'][0], df['40 a 59 anos'][1], df['60 a 79 anos'][2], df['mais 80 anos'][3]]

            # 2.3 - 1:1 : Plotagem da Visualização - Barra 05
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(name='População Total (2010)',
                                  x=values, y=y_pop,
                                  text=y_pop, textposition='auto',
                                  marker_color='#4169E1', marker_line_color="#0d0d0d", marker_line_width=1))
            fig1.add_trace(go.Bar(name='Vacinados',
                                  x=values, y=y_vac,
                                  text=y_vac, textposition='auto',
                                  marker_color='#D70270', marker_line_color="#0d0d0d", marker_line_width=1))
            fig1.update_layout(legend_font_size=10, autosize=False,
                               paper_bgcolor="#f0f0ff", plot_bgcolor="#f0f0ff",
                               font={'color': "#0d0d0d", 'family': "sans-serif"}, height=200, width=550,
                               margin=dict(l=5, r=5, b=5, t=5),
                               legend=dict(bordercolor="#0d0d0d", borderwidth=0.5,
                                           orientation="v",
                                           yanchor="top",
                                           y=0.95,
                                           xanchor="right",
                                           x=0.98),
                               barmode='group')
            fig1.update_xaxes(
                title_text='Faixa Etária',
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9))
            fig1.update_yaxes(
                title_text="Número de Residentes/Vacinados",
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                nticks=8, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

            st.markdown(html_card_header_2B_3_11, unsafe_allow_html=True)  #>População Total x População Vacinada</h5>
            st.plotly_chart(fig1, use_container_width=True)                # Gráfico de Barra 05
        with col3A:
            st.write("")
        with col4A:
            # 2.3 - 1.2 : Declaração de variáveis e Pré-Plot - Tabela 05
            df_filter2 = df_selection[["faixa_etaria", "Total Doses",
                                       "1° Dose", "2° Dose", "Dose Única", "Dose Reforco",
                                       "AstraZeneca", "Pfizer", "Coronavac", "Janssen"]]
            df_new2 = df_filter2.groupby('faixa_etaria').sum().reset_index()

            # 2.3 - 1:2 : Plotagem da Visualização - Tabela 05
            st.markdown(html_card_header_2B_3_12, unsafe_allow_html=True)   # >Dados Agrupados por Faixa Etária</h5>
            st.dataframe(data=df_new2, width=550, height=250)               # Tabela 05
        with col5A:
            st.write("")

    with st.container():
        col1B, col2B, col3B, col4B, col5B = st.columns([1, 20, 1, 20, 1])
        with col1B:
            st.write("")
        with col2B:
            # 2.3 - 2.1 : Declaração de variáveis e Pré-Plot - Linha 05
            df_area = df_selection.groupby(['vacina_dataAplicacao']).sum().reset_index()

            # 2.3 - 2.1 : Declaração de variáveis e Pré-Plot - Linha 05
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['menos 19 anos'],
                name='menos 19 anos',
                mode='lines',
                line=dict(width=1, color='#4169E1'),
                stackgroup='one'))
            fig1.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['20 a 39 anos'],
                name='20 a 39 anos',
                mode='lines',
                line=dict(width=1, color='#D70270'),
                stackgroup='two'))
            fig1.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['40 a 59 anos'],
                name='40 a 59 anos',
                mode='lines',
                line=dict(width=1, color='#00cccc'),
                stackgroup='three'))
            fig1.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['60 a 79 anos'],
                name='60 a 79 anos',
                mode='lines',
                line=dict(width=1, color='#8600b3'),
                stackgroup='four'))
            fig1.add_trace(go.Scatter(
                x=df_area['vacina_dataAplicacao'],
                y=df_area['mais 80 anos'],
                name='mais 80 anos',
                mode='lines',
                line=dict(width=1, color='#b3002d'),
                stackgroup='five'))
            fig1.update_layout(paper_bgcolor="#f0f0ff", plot_bgcolor="#f0f0ff",
                               font={'color': "#0d0d0d", 'family': "sans-serif"}, height=250, width=550,
                               margin=dict(l=5, r=5, b=5, t=5),
                               legend=dict(bordercolor="#0d0d0d", borderwidth=0.5,
                                           font_size=10, orientation="v",
                                           yanchor="top",
                                           y=0.98,
                                           xanchor="right",
                                           x=0.98))
            fig1.update_xaxes(
                title_text='Dias da Aplicação da Vacina',
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                rangeslider_visible=True, showgrid=False)
            fig1.update_yaxes(
                title_text="Número de Vacinados",
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

            st.markdown(html_card_header_2B_3_21, unsafe_allow_html=True) # >Variação diária de Vacinados</h5>
            st.plotly_chart(fig1)                                         # Gráfico de Linha 05
        with col3B:
            st.write("")
        with col4B:
            # 2.3 - 2.2 : Declaração de variáveis e Pré-Plot - Barra 06
            df = df_selection.groupby(['faixa_etaria']).sum().reset_index()

            values = ['menos 19 anos', '20 a 39 anos', '40 a 59 anos', '60 a 79 anos', 'mais 80 anos']
            y_1dose = [df['1° Dose'][4], df['1° Dose'][0], df['1° Dose'][1], df['1° Dose'][2], df['1° Dose'][3]]
            y_2dose = [df['2° Dose'][4], df['2° Dose'][0], df['2° Dose'][1], df['2° Dose'][2], df['2° Dose'][3]]
            y_Udose = [df['Dose Única'][4], df['Dose Única'][0], df['Dose Única'][1], df['Dose Única'][2], df['Dose Única'][3]]
            y_Adose = [df['Dose Reforco'][4], df['Dose Reforco'][0], df['Dose Reforco'][1], df['Dose Reforco'][2], df['Dose Reforco'][3]]

            # 2.3 - 2:2 : Plotagem da Visualização - Barra 06
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(name='1° Dose', x=values, y=y_1dose,
                                  text=y_1dose, textposition='auto',
                                  marker_color='#4169E1', marker_line_color="#0d0d0d", marker_line_width=1))
            fig2.add_trace(go.Bar(name='2° Dose', x=values, y=y_2dose,
                                  text=y_2dose, textposition='auto',
                                  marker_color='#D70270', marker_line_color="#0d0d0d", marker_line_width=1))
            fig2.add_trace(go.Bar(name='Dose Única', x=values, y=y_Udose,
                                  text=y_Udose, textposition='auto',
                                  marker_color='#4B0082', marker_line_color="#0d0d0d", marker_line_width=1))
            fig2.add_trace(go.Bar(name='Dose Reforço', x=values, y=y_Adose,
                                  text=y_Adose, textposition='auto',
                                  marker_color='#00cccc'))
            fig2.update_layout(legend_font_size=12, autosize=False,
                               paper_bgcolor="#f0f0ff", plot_bgcolor="#f0f0ff",
                               font={'color': "#0d0d0d", 'family': "sans-serif"}, height=250, width=550,
                               margin=dict(l=2, r=2, b=4, t=4),
                               legend=dict(bordercolor="#0d0d0d", borderwidth=0.5,
                                           orientation="v",
                                           yanchor="top",
                                           y=0.95,
                                           xanchor="right",
                                           x=0.98),
                               barmode='group')
            fig2.update_xaxes(
                title_text='Faixa Etária',
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9))
            fig2.update_yaxes(
                title_text="Doses Aplicadas",
                title_font=dict(family='Sans-serif', size=12),
                tickfont=dict(family='Sans-serif', size=9),
                nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

            st.markdown(html_card_header_2B_3_22, unsafe_allow_html=True)  #>Campanha de Vacinação - Doses Aplicadas</h5>
            st.plotly_chart(fig2)                                          # Gráfico de Barra 06

        with col5B:
            st.write("")

    return None


def mapas3( df_selection ):
    st.markdown("""---""")
    st.markdown(html_header_30, unsafe_allow_html=True)
    st.markdown("""---""")

    df_new = df_selection.groupby(["estabelecimento_municipio_nome", 'estalecimento_noFantasia', ]).sum().reset_index()
    df_new["Total Doses"] = df_new["1° Dose"] + df_new["2° Dose"] + df_new["Dose Única"] + df_new["Dose Reforco"]
    df_new = df_new[["estabelecimento_municipio_nome", "estalecimento_noFantasia", "Total Doses",
                     "1° Dose", "2° Dose", "Dose Única", "Dose Reforco",
                     "AstraZeneca", "Pfizer", "Coronavac", "Janssen",
                     "Feminino", "Masculino",
                     "BRANCA", "PRETA", "PARDA", "AMARELA", "INDIGENA",
                     'menos 19 anos', '20 a 39 anos', '40 a 59 anos', '60 a 79 anos', 'mais 80 anos']]

    st.markdown(html_card_header_3A_1_20, unsafe_allow_html=True)
    st.dataframe(data=df_new, width=1200, height=300)

    col1A, col2A, col3A, col4A, col5A = st.columns([1, 20, 1, 20, 1])
    with col1A:
        st.write("")
    with col2A:
        coordenadas = []
        for lat, long in zip(df_selection["lat"], df_selection["long"]):
            coordenadas.append([lat, long])

        mapa1 = folium.Map(location=[df_selection["lat"].mean(),
                                     df_selection["long"].mean()],
                           zoom_start=6, tiles='Stamen Terrain',
                           width=550, height=300, control_scale=True)

        mapa1.add_child(plugins.HeatMap(coordenadas))

        st.markdown(html_card_header_3A_1_11, unsafe_allow_html=True)
        folium_static(mapa1)

    with col3A:
        st.write("")
    with col4A:
        colors = {
            'FLORIANOPOLIS': 'green',
            'SAO JOSE': 'blue',
            'PALHOCA': 'red',
            'BIGUACU': 'orange',
            'BALNEARIO CAMBORIU': 'purple',
        }

        df_mapa2 = df_selection.groupby(['estalecimento_noFantasia',"estabelecimento_municipio_nome",
                                   "lat", "long", ]).count().reset_index()

        mapa2 = folium.Map(location=[df_mapa2["lat"].mean(),
                                     df_mapa2["long"].mean()],
                           zoom_start=10,
                           tiles='Stamen Terrain',
                           width=550, height=300, control_scale=True)

        # marker_cluster = MarkerCluster().add_to(mapa2)

        for name, row in df_mapa2.iterrows():
            if row['estabelecimento_municipio_nome'] in colors.keys():
                folium.Marker(
                    location=[row["lat"], row["long"]],
                    popup=f"""Estabelecimento:  {row['estalecimento_noFantasia']}
                                  Cidade:  {row['estabelecimento_municipio_nome']} 
                                  Vacinados: {row['paciente_id']}""",
                    icon=folium.Icon(color=colors[row['estabelecimento_municipio_nome']])
                ).add_to(mapa2)

        st.markdown(html_card_header_3A_1_12, unsafe_allow_html=True)
        folium_static(mapa2)

    with col5A:
        st.write("")

    return None