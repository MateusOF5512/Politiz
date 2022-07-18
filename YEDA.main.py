from YEDA_functions import *

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="YEDA - Your Exploratory Data Analysis", page_icon=":telescope:", layout="wide")


df = get_data_vac()
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
elif menu == '1 - Descrição da Campanha de Vacinação':
    teste1(df)
    rodape()
elif menu == '2 - Características da População Vacinada':
    rodape()
elif menu == "3 - Informações dos Postos de Vacinação":
    rodape()