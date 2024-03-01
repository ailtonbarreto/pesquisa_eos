import streamlit as st
import pandas as pd
import plotly_express as px


#-----------------------------------------------------------------------------------------------------------------------------
#Configuracao da pagina

st.set_page_config(page_title="Pesquisa de Satifação",layout="wide")

#layout
st.title("Pesquisa de Satisfação Janeiro 2024", anchor= False)
st.divider()
col1,col2,col3,col4, col5 = st.columns(5)
col6,col7 = st.columns(2)
col8, col9 = st.columns(2)
col10, = st.columns(1)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html = True)



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
df['Gestor'] = df['Quem é o seu Gestor (supervisor)?'].astype(str)
df = df.drop(columns="Quem é o seu Gestor (supervisor)?")
#-----------------------------------------------------------------------------------------------------------------------------
#dicionario notas

notas = {1: "Nenhum Pouco Feliz", 2: "Pouco Feliz", 3: "Feliz", 4: "Muito Feliz", 5: "Extremamente Feliz"}


df['Avaliação'] = df['Nivel de Felicidade'].map(notas)

#-----------------------------------------------------------------------------------------------------------------------------
#dataframe grafico de barras

dfbar = df
dfbar = dfbar.groupby(dfbar["Avaliação"])["Nivel de Felicidade"].count().reset_index()
dfbar = dfbar.sort_values("Nivel de Felicidade",ascending=False)

qtd_funcionario = 120

#-----------------------------------------------------------------------------------------------------------------------------
#dataframe grafico de valorizacao

dfpie = df["Valorização"].value_counts().reset_index()

#-----------------------------------------------------------------------------------------------------------------------------
#dataframe grafico conexao

dfpie_valor = df
dfpie_valor = df["Conexão com Colegas"].value_counts().reset_index()

#-----------------------------------------------------------------------------------------------------------------------------
#dataframe gestor

categorias = {'Muito bom': 'Muito bom','Ótimo': 'Ótimo','Bom': 'Bom','Ruim': 'Ruim','Péssimo': 'Péssimo','Excelente':'Excelente','Muito ruim':'Muito ruim'}




df['Categoria'] = df['Como você avalia o seu Gestor?'].map(categorias)


contagem_categorias = df['Categoria'].value_counts().sort_values(ascending=True)


df_count = len(df)
count_nao = (df['Valorização'] == 'Sim').sum()
nivel_satisfacao = (count_nao/df_count)*100
nivel_satisfacao = "{:.0f}%".format(nivel_satisfacao)

df_aprogestao = len(df)
count_sim = (df['Você Aprova a Forma como a Empresa é Dirigida?'] == 'Sim').sum()
aprovacao = (count_sim/df_aprogestao)*100
aprovacao = "{:.0f}%".format(aprovacao)



with col10:
    filtro_gestor = st.multiselect("Filtrar Gestor", df['Gestor'].unique(), default=df['Gestor'].unique())


contagem_avaliacoes = df.groupby(['Gestor', 'Como você avalia o seu Gestor?']).size().reset_index(name='Contagem')

contagem_avaliacoes = contagem_avaliacoes.query('Gestor == @filtro_gestor')

contagem_avaliacoes = contagem_avaliacoes.sort_values('Contagem',ascending=False)

df_felicidade = round(df['Nivel de Felicidade'].mean())


    

#-----------------------------------------------------------------------------------------------------------------------------
#charts


bar_chart = px.bar(dfbar, x="Nivel de Felicidade", y='Avaliação',orientation="h",title="Nível de Felicidade",
                   color_discrete_sequence=["#12b2fe","#00a8e8","#12b2fe","#d00000","#2ec4b6","#2ec4b6","#f94144"],color="Avaliação",
                   category_orders={'Avaliação':categorias})
                #    color_discrete_sequence=["#ffffff","#ffffff"])
bar_chart.update_xaxes(showgrid=False,visible = False)
bar_chart.update_traces(showlegend=False)
bar_chart.update_yaxes(showgrid=False,visible=True,title="")
bar_chart.layout.xaxis.fixedrange = True
bar_chart.layout.yaxis.fixedrange = True



pie_chart1 = px.pie(dfpie, names="Valorização", values='count',color_discrete_sequence=["#06d6a0","#e63946"],
                    title="Você sente-se valorizado pelo seu trabalho?",color='Valorização',category_orders={'Valorização':['Sim','Não']})

pie_chart_valor = px.pie(dfpie_valor,names='Conexão com Colegas',color_discrete_sequence=["#06d6a0","#e63946"],
                    category_orders={'Valorização':['Sim','Não']},color='Conexão com Colegas',
                    values='count',title='Sentimento de Conexão com Colegas')


#-----------------------------------------------------------------------------------------------------------------------------

bar_char_gestor = px.bar(contagem_categorias, x=contagem_categorias.values, y=contagem_categorias.index,color_discrete_sequence=["#ffffff","#ffffff"],
                title='Como Você Avalia seu Gestor',orientation='h')
bar_char_gestor.update_xaxes(showgrid=False,visible = False)
bar_char_gestor.update_traces(showlegend=False)
bar_char_gestor.update_yaxes(showgrid=False,visible=True,title="")
bar_char_gestor.layout.xaxis.fixedrange = True
bar_char_gestor.layout.yaxis.fixedrange = True





bar_char_avaliacao = px.bar(contagem_avaliacoes, x='Gestor', y="Contagem",orientation='v',category_orders={'Como você avalia o seu Gestor?':categorias},barmode="stack",
                    color_discrete_sequence=["#12b2fe","#00a8e8","#12b2fe","#d00000","#2ec4b6","#2ec4b6","#f94144"],
                    color='Como você avalia o seu Gestor?', title='Avaliações Por Gestor')
bar_char_avaliacao.update_xaxes(showgrid=False,visible = True)
bar_char_avaliacao.update_yaxes(showgrid=False,visible=False,title="")
bar_char_avaliacao.layout.xaxis.fixedrange = True
bar_char_avaliacao.layout.yaxis.fixedrange = True


#-----------------------------------------------------------------------------------------------------------------------------
#charts


with col1:  
    st.metric("Qtd Colaboradores",f'{qtd_funcionario} 👷‍♂️')
with col2:
    st.metric("Respostas",f'{df_count} 📝')
with col3:
    st.metric("Se Sentem Valorizados",f'{nivel_satisfacao} 🏆')    
with col4:
    st.metric("Média Felicidade",f'{df_felicidade} 😀')
with col5:
    st.metric("Aprovação Gestão",f'{aprovacao} 👍')

with col6:
    st.plotly_chart(bar_chart,use_container_width=True)
with col7:
    st.plotly_chart(pie_chart_valor,use_container_width=True)   
    
with col8:
    st.plotly_chart(bar_char_gestor,use_container_width=True)
with col9:
    st.plotly_chart(pie_chart1,use_container_width=True)

with col10:
    st.plotly_chart(bar_char_avaliacao,use_container_width=True)   

st.divider()
st.subheader('Acessar Pesquisa',anchor=False)
st.image("link.png",width=300)
st.link_button("Acessar",url ='https://docs.google.com/forms/d/e/1FAIpQLSeyzFMc7bFvPgmHreIAOhIWOB9PugK7NfAIpbEr6ReXJORfjg/viewform?usp=sf_link')
    
    
#-----------------------------------------------------------------------------------------------------------------------------
#CSS


borderselect = """
    <style>
    [data-testid="column"]
    {
    padding: 15px;
    background-color: #003459;
    border-radius: 12px;
    opacity: 85%;
    text-align: center;
    }
    </style>
"""
st.markdown(borderselect,unsafe_allow_html=True)


detalhes = """
    <style>
    [class="modebar-container"]
    {
    visibility: hidden;
    }
    </style>
"""


st.markdown(detalhes,unsafe_allow_html=True)

desativartelacheia = """
    <style>
    [data-testid="StyledFullScreenButton"]
    {
    visibility: hidden;
    }
    </style>
"""
st.markdown(desativartelacheia,unsafe_allow_html=True)



imagem = """
    <style>
    [class="st-emotion-cache-1kyxreq e115fcil2"]
    {
        align-items: center;
    }
    </style>
"""
st.markdown(imagem,unsafe_allow_html=True)