import streamlit as st
import pandas as pd
import numpy as np
from pandas import read_csv
from commom import commomHeader
import plotly as plty
import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #

st.set_page_config(layout="wide",page_title="Cana de Açucar",page_icon="chart_with_upwards_trend")
st.set_option('deprecation.showPyplotGlobalUse', False)
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Variáveis

arquiveList = [] # nome do arquivo
dfList = [] # dataFrame de cada arquivo
checkBoxList = [] # todos os checkbox

arquiveList2 = [] # nome do arquivo2
dfList2 = [] # dataFrame de cada arquivo2
checkBoxList2 = [] # todos os checkbox2

columnPlot = ['ChopperRPM','ChopperHydPrs','BHF','BaseCutRPM','BaseCutHght','BaseCutPrs','GndSpd','EngRPM','Js_1YAxPositn','Js_1XAxPositn','EngLoad','A2000_ChopperHydOilPrsHi','ChopperPctSetp','HydrostatChrgPrs']

def columnsNames():
    columns =  ['ChopperRPM','ChopperHydPrs','BHF','BaseCutRPM','BaseCutHght','BaseCutPrs','GndSpd','EngRPM','Js_1YAxPositn','Js_1XAxPositn','EngLoad','A2000_ChopperHydOilPrsHi','ChopperPctSetp','HydrostatChrgPrs','Off','Iddle','Waiting to Harvest','Moving','Harvesting','Choke Chopper','Reversion']
    
    return columns

def shortColumnsNames():
    columns =  ['Off','Iddle','Waiting to Harvest','Moving','Harvesting','Choke Chopper','Reversion']
    
    return columns

options = st.sidebar.selectbox(
    'Linechart_select Y variable',
    columnsNames())
correlogram=st.sidebar.checkbox("Correlograma",False)
histogram=st.sidebar.checkbox("Histograma",False)
options2 = st.sidebar.selectbox(
    'select state',
    shortColumnsNames())
multigram=st.sidebar.checkbox("MultiHist",False)
plot_fixed_mult=st.sidebar.checkbox("Plot Estático Multilinhas",False)


def selConName(colx, coly,df):
    df_filter = df.loc[:, [colx, coly]]
    df_filter.dropna(inplace = True)
    #print(df_filter.head())
    return df_filter[colx], df_filter[coly]

def selConNameManyDataset(coly,checkList,dfListOld,options2):
    # result=pd.Series()
    result=''
    dfs = []
    for idx,i in enumerate(checkList):
        if i == True:
            dfAdd = dfListOld[idx]
            dfs.append(dfAdd)
            

    contador = 0 # contador inicia em 0
    for df in dfs: # para cada df nos df's
        df_filter = df.loc[:, [coly]] # filtra as colunas
        df_filter.dropna(inplace = True) #apaga as linhas com registros nulos
        df_filter2 = df_filter[ df[options2] == 1]
        #print(df[options2].describe())
        #df_filter2 = df_filter
        if contador == 0: # caso contador for 0
            result = df_filter2[coly] # copia o valor do novo df filtrado para o result
        else: # caso for > 0
            result = pd.concat([result,df_filter2[coly]]) # junção dos valores das colunas de cada df
        contador +=1 # adiciona mais 1 no contador
        break
    # print(result.shape) # printa o formato total do result
    return result # retorna o result 

#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#
def incluiCondicaoTrabalho(dfOrigin):

    condicao1 = [(dfOrigin['EngRPM'] == 0)]
    opcoes1 =  [1]
    dfOrigin["Off"] = np.select(condicao1, opcoes1,)

    condicao2 = [(dfOrigin["BHF"] == 0) & (dfOrigin["GndSpd"] < 0.36)]
    opcoes2 =  [1]
    dfOrigin["Iddle"] = np.select(condicao2, opcoes2,)

    condicao3 = [(dfOrigin["BHF"] == 1) & (dfOrigin["BaseCutPrs"] < 5)]
    opcoes3 =  [1]
    dfOrigin["Waiting to Harvest"] = np.select(condicao3, opcoes3,)

    condicao4 = [(dfOrigin["BHF"] == 0)  & (dfOrigin["GndSpd"] >= 0.36)]
    opcoes4 =  [1]
    dfOrigin["Moving"] = np.select(condicao4, opcoes4,)

    condicao5 = [ (dfOrigin["BHF"] == 1) & (dfOrigin["BaseCutPrs"] >= 40) ]
    opcoes5 =  [1]
    dfOrigin["Harvesting"] = np.select(condicao5, opcoes5,)

    condicao6 = [(dfOrigin['A2000_ChopperHydOilPrsHi'] == 1)]
    opcoes6 =  [1]
    dfOrigin["Choke Chopper"] = np.select(condicao6, opcoes6,)

    condicao7 = [(dfOrigin["BHF"] == 2)]
    opcoes7 =  [1]
    dfOrigin["Reversion"] = np.select(condicao7, opcoes7,)
#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#

col1,col2 = st.columns(2)
with col1:
    uploaded_files = st.file_uploader("Choose a CSV_Old file", accept_multiple_files=True,type=['csv'])
    for uploaded_file in uploaded_files:
        arquiveList.append(uploaded_file.name)
        df = read_csv(uploaded_file,sep=";")
        df.rename(columns={"Time [s]": "Time"}, inplace= True)
        incluiCondicaoTrabalho(df)
        dfOrigin=df.copy()
        dfList.append(df)
with col2:
    uploaded_files2 = st.file_uploader("Choose a CSV_New file", accept_multiple_files=True,type=['csv'])
    for uploaded_file in uploaded_files2:
        arquiveList2.append(uploaded_file.name)
        df = read_csv(uploaded_file,sep=";")
        df.rename(columns={"Time [s]": "Time"}, inplace= True)
        incluiCondicaoTrabalho(df)
        dfOrigin=df.copy()
        dfList2.append(df)

if len (dfList) != 0:

    for i in range(len(arquiveList)):
        nomeArquivo = f"arquivoOld {i+1}"
        checkBoxList.append(st.sidebar.checkbox(nomeArquivo,False)) 

if len (dfList2) != 0:

    for i in range(len(arquiveList2)):
        nomeArquivo = f"arquivoNew {i+1}"
        checkBoxList2.append(st.sidebar.checkbox(nomeArquivo,False)) 


#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#

if plot_fixed_mult:
    idSelected = []
    eixoAxs=[]

    plt.figure(figsize=(20,18))
    for idx,checkB in enumerate(checkBoxList):
        if checkB:
            idSelected.append(idx)
                
    totalItems = (len(idSelected))

    if totalItems == 0:
        st.error('Nenhum Arquivo Selecionado')
    else:
        
        if totalItems == 1:
            fig, axOne = plt.subplots(nrows=1, ncols=1,layout='constrained')
            eixoAxs.append(axOne)   

        else:
            fig,axs = plt.subplots(nrows=totalItems, ncols=1,layout='constrained')
            for grafico in axs:
                eixoAxs.append(grafico)

        for idx,ax in enumerate(eixoAxs):
            selectPosition=idSelected[idx]
            xValues, yValues = selConName("Time",options,dfList[selectPosition])
            ax.tick_params(labelsize=5)
            ax.scatter(xValues, yValues, s=0.5)
            ax.set_title(f'{arquiveList[selectPosition]} (Arquivo {selectPosition + 1})',fontsize=8)
            ax.grid(True)

        plt.gcf().set_size_inches(10, 8)  
        fig.tight_layout()
        fig.supxlabel( "     Time(s)",fontsize=5)
        
        st.pyplot(fig)

#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#
if correlogram:
    pass
# col1,col2 = st.columns(2)
# with col1:
#     val1 = st.selectbox('Valor 1',columnsNames())
# with col2:
#     val2 = st.selectbox('Valor 2',columnsNames())

#     plt.figure(figsize=(12,10), dpi= 80)
#     sns.heatmap(df.corr(), xticklabels=df.corr(val1), yticklabels=df.corr(val2), cmap='RdYlGn', center=0, annot=True)

#     # Decorations
#     # plt.title('Correlogram of mtcars', fontsize=22)
#     plt.xticks(fontsize=12)
#     plt.yticks(fontsize=12)
#     plt.show()

#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#
    
if histogram:

    #x,y = selConName("Time",options,dfList[0])
    old = selConNameManyDataset(options, checkBoxList,dfList, options)
    new = selConNameManyDataset(options, checkBoxList2,dfList2, options)

    #y = dfList[0] + dfList[1]
    print (len(old),len(new))
    bins = np.linspace(0, 20, 100)
    
    fig, axOne = plt.subplots(nrows=1, ncols=1,layout='constrained', figsize=(8,5))
    if len(new)!=0:
        axOne.hist(new, alpha=0.5, label="New",color="y")
    if len(old)!=0:
        axOne.hist(old, alpha=0.5, label="Old",color="r")
    axOne.grid(True)
    axOne.set_title(options,fontsize=10)
    #axOne.hist(y, bins, alpha=0.5, label='y')
    axOne.legend(loc='upper right')
    #plt.hist().set_size_inches(10, 8) 

    st.pyplot(fig)

   
if multigram:
    pass

    contador = 0
    axs = []

    plt.figure(figsize=(10,8))

    totalItems = len(columnPlot)

    if True: # 
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
    
    for idx, coly in enumerate(columnPlot):
         old = selConNameManyDataset(coly, checkBoxList,dfList,options2)
         new = selConNameManyDataset(coly, checkBoxList2,dfList2,options2)
         axs[idx].tick_params(labelsize=5)
         axs[idx].set_title(coly,fontsize=10)
         axs[idx].grid(True)
         axs[idx].hist(old,bins= 50, alpha=0.5, label="Old",color="y")
         axs[idx].hist(new,bins= 50, alpha=0.5, label="New",color="r")
         axs[idx].legend(loc='upper left', fontsize=5)
         print(options2)

    st.pyplot(fig)
    #print(columnChoose)










