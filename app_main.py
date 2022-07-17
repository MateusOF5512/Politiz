from app_functions import *

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Observatório de Dados Abertos", page_icon=":telescope:", layout="wide")


df = get_data_vac( path_vac )
df_selection = set_feature( df )
df_posto = get_data_posto( path_posto )
introd()

menu = st.selectbox("Selecione Aqui sua Análise Exploratória!",
                        ("Bem-vindo!",
                         "0 - Dicas de Exploração",
                         "1 - Descrição da Campanha de Vacinação",
                         "2 - Características da População Vacinada",
                         "3 - Informações dos Postos de Vacinação"
                         ))


if menu == 'Bem-vindo!':
    bem_vindo()
    rodape()
elif menu == '0 - Dicas de Exploração':
    como_usar()
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
    mapas3( df_selection, df_posto )
    rodape()