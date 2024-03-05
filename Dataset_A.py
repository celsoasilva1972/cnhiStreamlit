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
# def incluiCondicaoTrabalho(dfOrigin):
#      condicao1 = [(dfOrigin['BHF'] == 1) & (dfOrigin['BaseCutHght'] <= 100) & (dfOrigin['BaseCutPrs'] != 0) & (dfOrigin['BaseCutRPM'] != 0) & ( dfOrigin['BaseCutPrs'] != 0 ) &  (dfOrigin['GndSpd'] != 0) & (dfOrigin['EngRPM'] != 0) ]
#      opcoes1 = [1]
#      dfOrigin["Colhendo"] = np.select(condicao1, opcoes1,)

#      condicao2 = [(dfOrigin['BHF'] == 1)  & ( dfOrigin['BaseCutPrs'] <= 0.01) &  (dfOrigin['GndSpd'] != 0) & (dfOrigin['EngRPM'] != 0) ]
#      opcoes2 = [1]
#      dfOrigin["NaoColhendoEmMovimento"] = np.select(condicao2, opcoes2, )

#      condicao3 = [(dfOrigin['GndSpd'] <= 0.01)  & ((dfOrigin['BHF'] == 0) | (dfOrigin['BHF'] == 1)) ] 
#      opcoes3 = [1]
#      dfOrigin["Parado"] = np.select(condicao3, opcoes3, )   
# def incluiCondicaoTrabalho(dfOrigin):
#     condicao1 = [(dfOrigin['ChopperRPM'] == 0) 
#                  & (dfOrigin["ChopperHydPrs"] == 0) 
#                  & (dfOrigin["BHF"] == 0) 
#                  & (dfOrigin["BaseCutRPM"] == 0) 
#                  & (dfOrigin["BaseCutPrs"] == 0) 
#                  & (dfOrigin["GndSpd"] == 0) 
#                  & (dfOrigin['EngRPM'] == 0) 
#                  & (dfOrigin['A2000_ChopperHydOilPrsHi'] == 0) 
#                  & (dfOrigin["HydrostatChrgPrs"] == 0)]
#     opcoes1 =  [1]
#     dfOrigin["Off"] = np.select(condicao1, opcoes1,)

#     condicao2 = [(dfOrigin['ChopperRPM'] == 0) 
#                  & (dfOrigin["ChopperHydPrs"] <= 30) 
#                  & (dfOrigin["BHF"] == 0) 
#                  & (dfOrigin["BaseCutRPM"] == 0) 
#                  & (dfOrigin["BaseCutPrs"] == 0) 
#                  & (dfOrigin["GndSpd"] == 0) 
#                  & (dfOrigin['EngRPM'] == 800) 
#                  & (dfOrigin['EngLoad'] <= 20) 
#                  & (dfOrigin['A2000_ChopperHydOilPrsHi'] == 0) 
#                  & (dfOrigin["HydrostatChrgPrs"] >= 18.0)&(dfOrigin["HydrostatChrgPrs"] <= 28.0)
#                  ]
#     opcoes2 =  [1]
#     dfOrigin["PontoMorto"] = np.select(condicao2, opcoes2,)

#     condicao3 = [(dfOrigin['ChopperRPM'] >= 170) & (dfOrigin['ChopperRPM'] <= 190)
#                  & (dfOrigin["ChopperHydPrs"] <= 60.00) 
#                  & (dfOrigin["BHF"] == 1) 
#                 #  & (dfOrigin["BaseCutRPM"] == 0) 
#                 #  & (dfOrigin["BaseCutPrs"] <= 5) 
#                  & (dfOrigin["GndSpd"] == 0) 
#                  & (dfOrigin['EngRPM']  >=801)  & (dfOrigin['EngRPM']  <=1600) 
#                  & (dfOrigin['A2000_ChopperHydOilPrsHi'] == 0) 
#                 #  & (dfOrigin["HydrostatChrgPrs"] >= 18.0)&(dfOrigin["HydrostatChrgPrs"] <= 28.0)
#                  ]
                 
#     opcoes3 =  [1]
#     dfOrigin["EsperandoColheita"] = np.select(condicao3, opcoes3,)

#     condicao4 = [(dfOrigin['ChopperRPM'] <= 10) 
#                  & (dfOrigin["ChopperHydPrs"] <= 30.00) 
#                  & (dfOrigin["BHF"] == 0) 
#                  & (dfOrigin["BaseCutRPM"] == 0) 
#                  & (dfOrigin["BaseCutPrs"] <= 10) 
#                  & (dfOrigin["GndSpd"] > 0) 
#                 #  & (dfOrigin['A2000_ChopperHydOilPrsHi'] == 0) 
#                 #  &  (dfOrigin["HydrostatChrgPrs"] >= 18.0)
#                 #  &(dfOrigin["HydrostatChrgPrs"] <= 28.0)
#                  ]
#     opcoes4 =  [1]
#     dfOrigin["Movendo"] = np.select(condicao4, opcoes4,)

#     condicao5 = [(dfOrigin['ChopperRPM'] <= 177) 
#                  & (dfOrigin["ChopperHydPrs"] >= 20.00) 
#     #              & (dfOrigin["BHF"] == 1) 
#     #              & (dfOrigin["BaseCutRPM"] > 515) 
#     #              & (dfOrigin["BaseCutHght"] <= 100) 
#     #              & (dfOrigin["BaseCutPrs"] >= 40) 
#     #              & (dfOrigin["GndSpd"]  <=10.0) 
#     #              & (dfOrigin["GndSpd"]  >=0.5 ) 
#     #              & (dfOrigin['EngRPM'] <= 1699) 
#     #              & (dfOrigin['EngLoad'] >40 ) 
#     #              & (dfOrigin['A2000_ChopperHydOilPrsHi'] == 0) 
#                 #  & (dfOrigin["HydrostatChrgPrs"] >= 18.0)&(dfOrigin["HydrostatChrgPrs"] <= 28.0)
#                  ]
#     opcoes5 =  [1]
#     dfOrigin["Colhendo"] = np.select(condicao5, opcoes5,)

#     condicao6 = [(dfOrigin['ChopperRPM'] > 177) 
#                  & (dfOrigin["ChopperHydPrs"] > 80) 
#                  & (dfOrigin["BHF"] == 1) 
#                  & (dfOrigin["BaseCutRPM"] > 515) 
#                  & (dfOrigin["BaseCutHght"] <= 100) 
#                  & (dfOrigin["BaseCutPrs"] >= 40) 
#                  & (dfOrigin["GndSpd"]  <=10.0) 
#                  & (dfOrigin["GndSpd"]  >=0.5 ) 
#                  & (dfOrigin['EngRPM']  <= 1699) 
#                  & (dfOrigin['EngLoad'] >=50) 
#                  & (dfOrigin['A2000_ChopperHydOilPrsHi'] == 1) 
#                  & (dfOrigin["HydrostatChrgPrs"] >= 18.0)&(dfOrigin["HydrostatChrgPrs"] <= 28.0)
#                  ]
#     opcoes6 =  [1]
#     dfOrigin["Embuchado"] = np.select(condicao6, opcoes6,)

#     condicao7 = [(dfOrigin['ChopperRPM'] >= 255) 
#                  & (dfOrigin["ChopperHydPrs"] <= 25) 
#                  & (dfOrigin["BHF"] == 2) 
#                  & (dfOrigin["BaseCutRPM"] == 630) 
#                  & (dfOrigin["BaseCutHght"] >= 300) 
#                  & (dfOrigin["BaseCutPrs"] <= 25) 
#                  & (dfOrigin["GndSpd"] <= 3) 
#                  & (dfOrigin['EngRPM'] >= 1700) 
#                  & (dfOrigin['EngLoad'] >=50) 
#                  & (dfOrigin['A2000_ChopperHydOilPrsHi'] == 0) 
#                  & (dfOrigin["HydrostatChrgPrs"] >= 18.0)
#                  & (dfOrigin["HydrostatChrgPrs"] <= 28.0)
#                  ]
#     opcoes7 =  [1]
#     dfOrigin["Reversao"] = np.select(condicao7, opcoes7,)


def incluiCondicaoTrabalho(dfOrigin):
    condicao1 = [(dfOrigin['ChopperRPM'] == 0)]
    opcoes1 =  [1]
    dfOrigin["Off"] = np.select(condicao1, opcoes1,)

    condicao2 = [(dfOrigin["BHF"] == 0) & (dfOrigin["GndSpd"] >= 10)]
    opcoes2 =  [1]
    dfOrigin["PontoMorto"] = np.select(condicao2, opcoes2,)
    
    condicao3 = [(dfOrigin["ChopperHydPrs"] <= 60.00) & (dfOrigin["BHF"] == 1)]
                 
    opcoes3 =  [1]
    dfOrigin["EsperandoColheita"] = np.select(condicao3, opcoes3,)

    condicao4 = [(dfOrigin["BHF"] == 0) & (dfOrigin["GndSpd"] >= 10) ]
    opcoes4 =  [1]
    dfOrigin["Movendo"] = np.select(condicao4, opcoes4,)

    condicao5 = [(dfOrigin["BHF"] == 1) & (dfOrigin["BaseCutPrs"] >= 40) ]
    opcoes5 =  [1]
    dfOrigin["Colhendo"] = np.select(condicao5, opcoes5,)

    condicao6 = [(dfOrigin['A2000_ChopperHydOilPrsHi'] == 1)]
    opcoes6 =  [1]
    dfOrigin["Embuchado"] = np.select(condicao6, opcoes6,)

    condicao7 = [(dfOrigin["BHF"] == 2)]
    opcoes7 =  [1]
    dfOrigin["Reversao"] = np.select(condicao7, opcoes7,)

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
                    incluiCondicaoTrabalho(df)
                    dfOrigin=df.copy()

                    # incluiCondicaoTrabalho(dfOrigin)               
                    #df=(df-df.mean())/df.std()
                    st.session_state['dfGeral'] = df
                    st.session_state['dfOrigin'] = dfOrigin

        else:
            df = st.session_state['dfGeral']
            dfOrigin = st.session_state['dfOrigin']
        
    else:
        st.error('Arquivo ainda não foi importado')
    return df, dfOrigin

def columnsNames():
    columns =  ['ChopperRPM','ChopperHydPrs','BHF','BaseCutRPM','BaseCutHght','BaseCutPrs','GndSpd','EngRPM','Js_1YAxPositn','Js_1XAxPositn','EngLoad','A2000_ChopperHydOilPrsHi','ChopperPctSetp','HydrostatChrgPrs','Off','PontoMorto','EsperandoColheita','Movendo','Colhendo','Embuchado','Reversao']
    return columns

def selConName(colx, coly, df):
    df_filter = df.loc[:, [colx, coly]]
    df_filter.dropna(inplace = True)
    #print(df_filter.head())
    return df_filter[colx], df_filter[coly]


def showAllColumnsByRow(df, xColumnName, columnChoose, LabelDict):
    contador = 0
    axs = []

    plt.figure(figsize=(10,8))

    totalItems = len(columnChoose)

    if totalItems == 0:
        st.error('Nenhuma linha selecionada')
        return
    if totalItems == 1:
    #    plt.figure(figsize=(20,2))
       fig, axIndefined = plt.subplots(nrows=1, ncols=1,layout='constrained')
       axs.append(axIndefined)    
    elif totalItems <= 3:
    #    plt.figure(figsize=(5,3))
       fig, axIndefined = plt.subplots(nrows=totalItems, ncols=1,layout='constrained')
       axs = axIndefined
    else: # >= 4
    #    plt.figure(figsize=(5,3))
       rows = (totalItems // 2) + totalItems % 2
       fig, axIndefined = plt.subplots(nrows=rows,ncols=2,layout='constrained')
       if (totalItems % 2) == 1 :
        axIndefined[-1,-1].axis('off')

       for line in range(rows):
           axs.append(axIndefined[line][0])
       for line in range(rows):
           axs.append(axIndefined[line][1])
       plt.gcf().set_size_inches(10, 8)     
    
    for idx, coly in enumerate(columnChoose):
         xValues, yValues = selConName(xColumnName,coly,df)
         axs[idx].tick_params(labelsize=5)
         axs[idx].scatter(xValues, yValues, s=0.5)
         axs[idx].set_ylabel(tratarLabel(coly , LabelDict[coly]),fontsize=8)

         axs[idx].grid(True)
         contador += 1

    fig.tight_layout()
    fig.supxlabel( "            Time(s)",fontsize=10)
    
    st.pyplot(fig)
    print(columnChoose)


def getUnidadeLabels():
    unidadesDict = {}
    for name in columnsNames() :
        unidadesDict[name] = ''
        unidadesDict['ChopperHydPrs'] = '\n(bar)'
        unidadesDict['ChopperRPM'] = '\n(rpm)'
        unidadesDict['BaseCutPrs'] = '\n(bar)'
        unidadesDict['BaseCutRPM'] = '\n(rpm)'
        unidadesDict['GndSpd'] = '\n(km/h)'
        unidadesDict['EngRPM'] = '\n(rpm)'
        unidadesDict['EngLoad'] = '\n(%)'
        unidadesDict['BaseCutHght'] = '\n(%)'
        unidadesDict['ChopperPctSetp'] = '\n(%)'
        unidadesDict['HydrostatChrgPrs'] = '\n(bar)'
        unidadesDict['A2000_ChopperHydOilPrsHi'] = '\n(bin)'
        unidadesDict['BHF'] = '\n(bin)'
        unidadesDict['Js_1YAxPositn'] = '\n(?)'
        unidadesDict['Js_1XAxPositn'] = '\n(?)'


    return unidadesDict

def tratarLabel (coluna,unidade):
    fim = 10
#    for name in coluna():
    if coluna == 'ChopperHydPrs':
        return 'ChopHPr' + unidade
    if coluna == 'ChopperRPM':
        return 'ChopRPM' + unidade
    if coluna == 'BaseCutPr':
        return 'BaseCPr' + unidade
    if coluna == 'BaseCutHght':
        return 'BaseCutHg' + unidade
    if coluna == 'ChopperPctSetp':
        return 'ChopPct' + unidade
    if coluna == 'BaseCutRPM':
        return 'BaseCRPM' + unidade
    if coluna == 'A2000_ChopperHydOilPrsHi':
        return 'A2000Chop' + unidade
    

    juncao = f'{coluna[0:fim]} {unidade}'
    return juncao      

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Desenha o header de todas as páginas
commomHeader(st)


# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Barra Lateral

# Check Box normalização
normalizadoCheckbox = st.sidebar.checkbox("normalizado",False)

# Variáveis do df original normalizado
options = st.sidebar.multiselect(
    'Linechart_select Y variable',
    columnsNames(),
    ['BaseCutRPM'])



# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Variáveis de novas variáveis de acordo com condições de trabalho

#Trabalho = st.sidebar.multiselect(
#    'Linechart_select Y variable',
#    ['Working','Runing','stoped'],
#    ['Working'])

# Trabalho = st.sidebar.multiselect(
#     'Linechart_select Y variable',
#     ['Colhendo','NaoColhendoEmMovimento','Parado'],
#     ['Colhendo'])
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Check Box

w1 = st.sidebar.checkbox("show table", False)
linechart_select=st.sidebar.checkbox("Linechart_select",False)
# linechart_Origin=st.sidebar.checkbox("Linechart_Origin",False)
# linechart_full=st.sidebar.checkbox("Linechart_full",False)
# plot_fixed=st.sidebar.checkbox("Plot não Iterativo",False)
plot_fixed_mult=st.sidebar.checkbox("Plot Estático Multilinhas",False)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Separação da página por Colunas


dfGeral, dfOrigin = lerArquivo()

col1,col2 = st.columns(2)

with col1:
    if len(dfGeral) != 0: 
        if normalizadoCheckbox:
            dfGeral=(dfGeral-dfGeral.min())/(dfGeral.max()-dfGeral.min())
            dfGeral["Time"]=dfOrigin["Time"]

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Gráfico de linhas com varíáveis específicas do dataset normalizado pelo Tempo
    if len(dfGeral) != 0:   
        if linechart_select:
            print('$$$$$$$$$$$$ linechart_selected')
            st.subheader("Line Chart Select")
            st.line_chart(dfGeral,x="Time",y=options)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Gráfico de linhas com todas as novas varíáveis específicas de trabalho pelo Tempo
    # if len(dfGeral) != 0:     
    #     if linechart_Origin:
    #         st.subheader("Line Chart Origin")
    #         st.line_chart(dfOrigin,x="Time",y=Trabalho) 
              
        
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Tabela do DataFrame
with col2:
    if len(dfGeral) != 0: 
        if w1:
            st.dataframe(dfOrigin,width=2000,height=550)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Gráfico de linhas com todas as varíáveis pelo Tempo

# if linechart_full:
# 	st.subheader("Line Chart Full")
# 	st.line_chart(dfGeral)

# if plot_fixed:
#     #arr = np.random.normal(1, 1, size=100)
#     #fig, ax = plt.subplots()
#     #ax.hist(arr, bins=20)
#     #st.pyplot(fig)
#     st.subheader("Line Chart Full")
#     someColors = ['black', 'blue', 'brown', 'coral', 'crimson', 'gold', 'green', 'grey', 'orange', 'purple','yellow', 'red', 'silver', 'violet', 'darkgreen']
#     showAllColumns(dfGeral, 'Time',options, someColors)

if plot_fixed_mult:
    #arr = np.random.normal(1, 1, size=100)
    #fig, ax = plt.subplots()
    #ax.hist(arr, bins=20)
    #st.pyplot(fig)

    if len(dfGeral) != 0:
    
        st.subheader("Plot em gráficos separados")
        #color = ['black', 'blue', 'brown', 'coral', 'crimson', 'gold', 'green', 'grey', 'orange', 'purple','yellow', 'red', 'silver', 'violet', 'darkgreen']
        labelDict = getUnidadeLabels()

        showAllColumnsByRow(dfGeral,'Time',options, labelDict)

    # st.subheader("Line Chart Full")
    # someColors = ['black', 'blue', 'brown', 'coral', 'crimson', 'gold', 'green', 'grey', 'orange', 'purple','yellow', 'red', 'silver', 'violet', 'darkgreen']
    # showAllColumns(dfGeral, 'Time',options, someColors, st)
