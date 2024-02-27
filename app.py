import streamlit as st
import pandas as pd
import plotly_express as px


#-----------------------------------------------------------------------------------------------------------------------------
#Configuracao da pagina

st.set_page_config(page_title="Pesquisa de Satifação",layout="wide")

#layout

col1,col2 = st.columns(2)
col3,col4 = st.columns(2)

#-----------------------------------------------------------------------------------------------------------------------------
#link da planilha de respostas

url = "https://docs.google.com/spreadsheets/d/1Q7ZgbtQakLOkDdUJ96seQKcUKjL4VPkJO_PvP7GW6ss/export?format=csv"

#-----------------------------------------------------------------------------------------------------------------------------
#ETL

df = pd.read_csv(url)
df['Nivel de Felicidade'] = df['Quão feliz você está no trabalho?'].astype(float)
df['Nivel de Felicidade'] = df['Nivel de Felicidade'].astype(int)
df = df.drop(columns="Quão feliz você está no trabalho?")
df["Valorização"] = df['Você sente-se valorizado pelo seu trabalho?'].astype(str)
df['Conexão com Colegas'] = df['Você sente-se conectado com seus colegas de trabalho?'].astype(str)
df = df.drop(columns="Você sente-se conectado com seus colegas de trabalho?")

#-----------------------------------------------------------------------------------------------------------------------------
#dicionario notas

notas = {1: "Nenhum Pouco Feliz", 2: "Pouco Feliz", 3: "Feliz", 4: "Muito Feliz", 5: "Extremamente Feliz"}


df['Avaliação'] = df['Nivel de Felicidade'].map(notas)

#-----------------------------------------------------------------------------------------------------------------------------
#dataframe grafico de barras

dfbar = df
dfbar = dfbar.groupby(dfbar["Avaliação"])["Nivel de Felicidade"].count().reset_index()
dfbar = dfbar.sort_values("Nivel de Felicidade")

# gestores = st.selectbox("Gestores",df['Quem é o seu Gestor (supervisor)?'].unique())
# df_gestor = df.query('`Quem é o seu Gestor (supervisor)?` in @gestores')


#dataframe grafico de valorizacao

dfpie = df["Valorização"].value_counts().reset_index()

#dataframe grafico conexao

dfpie_valor = df
dfpie_valor = df["Conexão com Colegas"].value_counts().reset_index()

#dataframe gestor

categorias = {'Muito bom': 'Muito bom','Ótimo': 'Ótimo','Bom': 'Bom','Ruim': 'Ruim','Péssimo': 'Péssimo','Excelente':'Excelente','Muito ruim':'Muito ruim'}


df['Categoria'] = df['Como você avalia o seu Gestor?'].map(categorias)


contagem_categorias = df['Categoria'].value_counts().sort_values(ascending=True)
# contagem_categorias = df_gestor['Categoria'].astype(int)


#-----------------------------------------------------------------------------------------------------------------------------
#charts


bar_chart = px.bar(dfbar, x="Nivel de Felicidade", y='Avaliação',orientation="h",title="Nível de Felicidade")

pie_chart = px.pie(dfpie, names=["Sim", "Não"], values='Valorização',title="Você sente-se valorizado pelo seu trabalho?")

pie_chart_valor = px.pie(dfpie_valor,names=["Sim", "Não"],values='Conexão com Colegas',title='Sentimento de Conexão com Colegas')

bar_char_gestor = px.bar(contagem_categorias, x=contagem_categorias.values, y=contagem_categorias.index, title='Como Você Avalia seu Gestor',orientation='h')

with col1:
    st.plotly_chart(bar_chart)

with col2:
    st.plotly_chart(pie_chart)

with col3:
    st.plotly_chart(pie_chart_valor)

with col4:
    st.plotly_chart(bar_char_gestor)