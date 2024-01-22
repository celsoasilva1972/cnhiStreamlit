import streamlit as st
import pandas as pd
import numpy as np
import plotly as plt
import matplotlib.pyplot as plt
from pandas import read_csv
from commom import commomHeader, showAllColumns


# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# configurações de sessão

if 'arquivo' not in st.session_state:
    st.session_state['initArquivo'] = 0

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# configurações da página
st.set_page_config(layout="wide",page_title="Cana de Açucar",page_icon="chart_with_upwards_trend")

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# funções

#def incluiCondicaoTrabalhoOld(dfOrigin):
    # condicao1 = [(dfOrigin['BHF'] == 1) & (dfOrigin['BaseCutHght'] <= 330) & (dfOrigin['GndSpd'] != 0) & (dfOrigin['EngRPM'] != 0)]
    # opcoes1 = [1]
    # dfOrigin["Working"] = np.select(condicao1, opcoes1,)

    # condicao2 = [
    # (dfOrigin['BHF']== 1) & (dfOrigin['GndSpd'] != 0) & (dfOrigin['EngRPM'] == 0)] 
    # opcoes2 = [1]
    # dfOrigin["Runing"] = np.select(condicao2, opcoes2, )

    # condicao3 = [
    # ((dfOrigin['BHF']== 1) |(dfOrigin['BHF']== 0)) & (dfOrigin['GndSpd'] == 0)] 
    # opcoes3 = [1]
    # dfOrigin["stoped"] = np.select(condicao3, opcoes3, )     


#-------------------------------------------------------------------------------------------------------------------------
def incluiCondicaoTrabalho(dfOrigin):
     condicao1 = [(dfOrigin['BHF'] == 1) & (dfOrigin['BaseCutHght'] <= 100) & (dfOrigin['BaseCutPrs'] != 0) & (dfOrigin['BaseCutRPM'] != 0) & ( dfOrigin['BaseCutPrs'] != 0 ) &  (dfOrigin['GndSpd'] != 0) & (dfOrigin['EngRPM'] != 0) ]
     opcoes1 = [1]
     dfOrigin["Colhendo"] = np.select(condicao1, opcoes1,)

     condicao2 = [(dfOrigin['BHF'] == 1)  & ( dfOrigin['BaseCutPrs'] <= 0.01) &  (dfOrigin['GndSpd'] != 0) & (dfOrigin['EngRPM'] != 0) ]
     opcoes2 = [1]
     dfOrigin["NaoColhendoEmMovimento"] = np.select(condicao2, opcoes2, )

     condicao3 = [(dfOrigin['GndSpd'] <= 0.01)  & ((dfOrigin['BHF'] == 0) | (dfOrigin['BHF'] == 1)) ] 
     opcoes3 = [1]
     dfOrigin["Parado"] = np.select(condicao3, opcoes3, )   


def lerArquivo():
    arquivo = st.file_uploader("Escolha um arquivo CSV",type=['csv'])

    df = pd.DataFrame()
    dfOrigin = pd.DataFrame()
    if arquivo:
        print(f'#####Arquivo lido ={arquivo.name} : {arquivo.type}')
        if st.session_state['initArquivo'] == 0:
            st.session_state['arquivo'] = arquivo
        oldArquivo = st.session_state['arquivo']
        if (oldArquivo != arquivo) or (st.session_state['initArquivo'] == 0):
            st.session_state['initArquivo'] = 1
            print(f'@@@@@@ arquivos diferentes: {oldArquivo.name} != {arquivo.name}')
            st.session_state['arquivo'] = arquivo
            match arquivo.type.split('/'):
                case 'text','csv':
                    df = read_csv(arquivo,sep =";")
                                
                    df.dtypes[df.dtypes == 'int64'] 

                    df.replace(np.nan,0,inplace=True)
                    
                    df.rename(columns={"Time [s]": "Time"}, inplace= True)
                    dfOrigin=df.copy()

                    incluiCondicaoTrabalho(dfOrigin)               
                    #df=(df-df.mean())/df.std()
                    st.session_state['dfGeral'] = df
                    st.session_state['dfOrigin'] = dfOrigin

        else:
            df = st.session_state['dfGeral'] 
            dfOrigin = st.session_state['dfOrigin']
        
    else:
        st.error('Arquivo ainda não foi importado')
    return df, dfOrigin
#teste----------------------------------------------------------------------------------------------------
def selConName(colx, coly, df):
    df_filter = df.loc[:, [colx, coly]]
    df_filter.dropna(inplace = True)
    #print(df_filter.head())
    return df_filter[colx], df_filter[coly]

# def showAllColumns(df, xColumnName, columnChoose, someColors):
#     contador = 0
#     plt.figure(figsize=(20,10))
#     fig, ax = plt.subplots()
#     for coly in columnChoose:
#          xValues, yValues = selConName(xColumnName,coly,df)
#          ax.plot(xValues, yValues,color=someColors[contador], label=coly)
#          contador += 1
#     #ax.legend()
#     #ax.xlabel(xColumnName);
#     #ax.ylabel('Values');
#     #ax.title('ALL SINALS') 
#     st.pyplot(fig)
#     print(columnChoose)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Desenha o header de todas as páginas
commomHeader(st)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Barra Lateral

# Variáveis do df original normalizado
options = st.sidebar.multiselect(
    'Linechart_select Y variable',
    ['ChopperRPM','ChopperHydPrs','BHF','BaseCutRPM','BaseCutHght','BaseCutPrs','GndSpd','EngRPM','Js_1YAxPositn','Js_1XAxPositn','EngLoad','A2000_ChopperHydOilPrsHi','ChopperPctSetp','HydrostatChrgPrs'],
    ['BaseCutRPM'])

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Check Box normalização
normalizadoCheckbox = st.sidebar.checkbox("normalizado",False)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Variáveis de novas variáveis de acordo com condições de trabalho

#Trabalho = st.sidebar.multiselect(
#    'Linechart_select Y variable',
#    ['Working','Runing','stoped'],
#    ['Working'])

Trabalho = st.sidebar.multiselect(
    'Linechart_select Y variable',
    ['Colhendo','NaoColhendoEmMovimento','Parado'],
    ['Colhendo'])
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Check Box

w1 = st.sidebar.checkbox("show table", False)
linechart_select=st.sidebar.checkbox("Linechart_select",False)
linechart_Origin=st.sidebar.checkbox("Linechart_Origin",False)
linechart_full=st.sidebar.checkbox("Linechart_full",False)
plot_fixed=st.sidebar.checkbox("Plot Estático",False)
plot_fixed_mult=st.sidebar.checkbox("Plot Estático Multilinhas",False)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Separação da página por Colunas


dfGeral, dfOrigin = lerArquivo()

col1,col2 = st.columns(2)

with col1:
    if normalizadoCheckbox:
        dfGeral=(dfGeral-dfGeral.min())/(dfGeral.max()-dfGeral.min())
        dfGeral["Time"]=dfOrigin["Time"]

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Gráfico de linhas com varíáveis específicas do dataset normalizado pelo Tempo
    if linechart_select:
        print('$$$$$$$$$$$$ linechart_selected')
        st.subheader("Line Chart Select")
        st.line_chart(dfGeral,x="Time",y=options)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Gráfico de linhas com todas as novas varíáveis específicas de trabalho pelo Tempo
    if linechart_Origin:
        st.subheader("Line Chart Origin")
        st.line_chart(dfOrigin,x="Time",y=Trabalho) 
              
        
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Tabela do DataFrame
with col2:
    if w1:
        st.dataframe(dfOrigin,width=2000,height=550)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Gráfico de linhas com todas as varíáveis pelo Tempo

if linechart_full:
	st.subheader("Line Chart Full")
	st.line_chart(dfGeral)

if plot_fixed:
    #arr = np.random.normal(1, 1, size=100)
    #fig, ax = plt.subplots()
    #ax.hist(arr, bins=20)
    #st.pyplot(fig)
    st.subheader("Line Chart Full")
    someColors = ['black', 'blue', 'brown', 'coral', 'crimson', 'gold', 'green', 'grey', 'orange', 'purple','yellow', 'red', 'silver', 'violet', 'darkgreen']
    showAllColumns(dfGeral, 'Time',options, someColors, st)

