import streamlit as st
import pandas as pd
import numpy as np
from pandas import read_csv
from matplotlib.ticker import PercentFormatter
#import seaborn as sns
import matplotlib.pyplot as plt
from util import renameColumns


# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #

st.set_page_config(layout="wide",page_title="Cana de Açucar",page_icon="chart_with_upwards_trend")
st.set_option('deprecation.showPyplotGlobalUse', False)
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Variáveis


arquiveList1 = [] # nome do arquivo1
dfList1 = [] # dataFrame de cada arquivo1
checkBoxList1 = [] # todos os checkbox1

arquiveList2 = [] # nome do arquivo2
dfList2 = [] # dataFrame de cada arquivo2
checkBoxList2 = [] # todos os checkbox2

arquiveList3 = [] # nome do arquivo3
dfList3 = [] # dataFrame de cada arquivo3
checkBoxList3 = [] # todos os checkbox3

arquiveList4 = [] # nome do arquivo4
dfList4 = [] # dataFrame de cada arquivo4
checkBoxList4 = [] # todos os checkbox4

columnPlot = ['ChopperRPM','ChopperHydPrs','BHF','BaseCutRPM','BaseCutHght','BaseCutPrs','GndSpd','EngRPM','Js_1YAxPositn','Js_1XAxPositn','EngLoad','A2000_ChopperHydOilPrsHi','ChopperPctSetp','HydrostatChrgPrs']
#columnPlot = ['ChopperRPM','ChopperHydPrs','BHF']#,'BaseCutRPM']
def columnsNames():
    columns =  ['ChopperRPM','ChopperHydPrs','BHF','BaseCutRPM','BaseCutHght','BaseCutPrs','GndSpd','EngRPM','Js_1YAxPositn','Js_1XAxPositn','EngLoad','A2000_ChopperHydOilPrsHi','ChopperPctSetp','HydrostatChrgPrs','Off','Iddle','Waiting to Harvest','Moving','Harvesting','Choke Chopper','Reversion']
    
    return columns

def shortColumnsNames():
    columns =  ['Off','Iddle','Waiting to Harvest','Moving','Harvesting','Choke Chopper','Reversion']
    
    return columns

# options = st.sidebar.selectbox('Linechart_select Y variable', columnsNames())
# plot_fixed_mult=st.sidebar.checkbox("Plot Estático Multilinhas",False)
# options2 = st.sidebar.selectbox('select state',shortColumnsNames())
# multigram=st.sidebar.checkbox("MultiHist",False)
# normalized = st.sidebar.checkbox("Normalizado",False)
# histogram=st.sidebar.checkbox("Histograma",False)
#correlogram=st.sidebar.checkbox("Correlograma",False)


def calculaHistPercent(dados):
        n, bins , _ = plt.hist(dados)
        porcentagem = 100 * n / np.sum(n)
        width = bins[1] - bins[0]
        print(f'width={width}')
        center = (bins[:-1] + bins[1:]) / 2
        plt.clf()
        return porcentagem, width, center

def getValuesHist(idx, allHistValues):
    porcentagem, width,  center = allHistValues[idx]
    return porcentagem, width,  center 

columnPlot = ['ChopperRPM','ChopperHydPrs','BHF','BaseCutRPM','BaseCutHght','BaseCutPrs','GndSpd','EngRPM','Js_1YAxPositn','Js_1XAxPositn','EngLoad','A2000_ChopperHydOilPrsHi','ChopperPctSetp','HydrostatChrgPrs']

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

def incluiCondicaoTrabalho(df):

    condicao1 = [(df['EngRPM'] == 0)]
    opcoes1 =  [1]
    df["Off"] = np.select(condicao1, opcoes1,)

    condicao2 = [(df["BHF"] == 0) & (df["GndSpd"] < 0.36)]
    opcoes2 =  [1]
    df["Iddle"] = np.select(condicao2, opcoes2,)

    condicao3 = [(df["BHF"] == 1) & (df["BaseCutPrs"] < 5.00)]
    opcoes3 =  [1]
    df["Waiting to Harvest"] = np.select(condicao3, opcoes3,)

    condicao4 = [(df["BHF"] == 0)  & (df["GndSpd"] >= 0.36)]
    opcoes4 =  [1]
    df["Moving"] = np.select(condicao4, opcoes4,)

    condicao5 = [ (df["BHF"] == 1) & (df["BaseCutPrs"] >= 40) ]
    opcoes5 =  [1]
    df["Harvesting"] = np.select(condicao5, opcoes5,)

    condicao6 = [(df['A2000_ChopperHydOilPrsHi'] == 1)]
    opcoes6 =  [1]
    df["Choke Chopper"] = np.select(condicao6, opcoes6,)

    condicao7 = [(df["BHF"] == 2)]
    opcoes7 =  [1]
    df["Reversion"] = np.select(condicao7, opcoes7,)
#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#


idSelected = []
eixoAxs=[]
tab1, tab2, tab3 = st.tabs(["MultiPlot", "MultiHist","correlogram"])

with tab1:

    col1,col2 = st.columns(2)
    with col1:
        uploaded_files1 = st.file_uploader("Choose a CSV file", accept_multiple_files=True,type=['csv'])
        for uploaded_file in uploaded_files1:
            arquiveList1.append(uploaded_file.name)
            df = read_csv(uploaded_file,sep=";")
            renameColumns(df)
            incluiCondicaoTrabalho(df)
            # if normalized:
            #     df=(df-df.min())/(df.max()-df.min())
          
            # dfOrigin=df.copy()
            dfList1.append(df)
            st.session_state['df'] = df
      
        
        
    with col2:

        options = st.selectbox('Linechart_select Y variable', columnsNames())
        for i in range(len(arquiveList1)):
            nomeArquivo = f"arquivo {i+1}"
            checkBoxList1.append(st.checkbox(nomeArquivo,False)) 
        with st.container():
        # if plot_fixed_mult:
            idSelected = []
            eixoAxs=[]
            plt.figure(figsize=(20,18))
            for idx,checkB in enumerate(checkBoxList1):
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
            xValues, yValues = selConName("Time",options,dfList1[selectPosition])
            ax.tick_params(labelsize=5)
            ax.scatter(xValues, yValues, s=0.5)
            ax.set_title(f'{arquiveList1[selectPosition]} (Arquivo {selectPosition + 1})',fontsize=8)
            ax.grid(True)

        plt.gcf().set_size_inches(10, 8)  
        fig.tight_layout()
        fig.supxlabel( "     Time(s)",fontsize=5)
        
        st.pyplot(fig)

        checks = st.columns(4)
            
with tab2:
    col3,col4,col5 = st.columns(3)

    with col3:
        uploaded_files2 = st.file_uploader("Choose a CSV_Old file", accept_multiple_files=True,type=['csv'])
        for uploaded_file in uploaded_files2:
            arquiveList2.append(uploaded_file.name)
            df = read_csv(uploaded_file,sep=";")
            renameColumns(df)
            incluiCondicaoTrabalho(df)
            dfList2.append(df)
            st.session_state['df'] = df

    with col4:
        uploaded_files3 = st.file_uploader("Choose a CSV_New file", accept_multiple_files=True,type=['csv'])
        for uploaded_file in uploaded_files3:
            arquiveList3.append(uploaded_file.name)
            df = read_csv(uploaded_file,sep=";")
            renameColumns(df)
            incluiCondicaoTrabalho(df)
            dfList3.append(df)
            st.session_state['df'] = df
    with col5:
        options2 = st.selectbox('select state',shortColumnsNames())

        if len (arquiveList2) != 0:
                
            for i in range(len(arquiveList2)):
                nomeArquivo = f"arquivoOld {i+1}"
                checkBoxList2.append(st.checkbox(nomeArquivo,False)) 

        if len (arquiveList3) != 0:

            for i in range(len(arquiveList3)):
                nomeArquivo = f"arquivoNew {i+1}"
                checkBoxList3.append(st.checkbox(nomeArquivo,False))
            # if multigram:
    contador = 0
    axs = []

    plt.figure(figsize=(10,8))

    totalItems = len(columnPlot)


    rows = (totalItems // 2) + totalItems % 2
    allHistValuesOld = {}
    allHistValuesNew = {}

    for idx, coly in enumerate(columnPlot):
        old = selConNameManyDataset(coly, checkBoxList2,dfList2,options2)
        new = selConNameManyDataset(coly, checkBoxList3,dfList3,options2)    
        # new = dados1[coly][:]
        # old = dados2[coly][:]
        porcentagem, width,  center = calculaHistPercent(old)
        allHistValuesOld[idx] = {}
        allHistValuesOld[idx] = [porcentagem,width, center]
        porcentagem, width,  center = calculaHistPercent(new)
        allHistValuesNew[idx] = {}
        allHistValuesNew[idx] = [porcentagem,width, center]    

    fig, axIndefined = plt.subplots(nrows=rows,ncols=2)#,layout='constrained')

    if (totalItems % 2) == 1 :
        axIndefined[-1,-1].axis('off')
    plt.gcf().set_size_inches(10, 8)

    for line in range(rows):
        axs.append(axIndefined[line][0])
    for line in range(rows):
        axs.append(axIndefined[line][1])

    for idx, coly in enumerate(columnPlot):
        axs[idx].tick_params(labelsize=5)
        axs[idx].set_title(coly,fontsize=5)
        axs[idx].grid(True)
        porcentagemOld, widthOld,  centerOld = getValuesHist(idx, allHistValuesOld)
        porcentagemNew, widthNew,  centerNew = getValuesHist(idx, allHistValuesNew)
        axs[idx].bar(centerOld, porcentagemOld, align='center', label="Old", width=widthOld, edgecolor='black',alpha=0.5)
        axs[idx].bar(centerNew, porcentagemNew, align='center',  label="New", width=widthNew, edgecolor='black',alpha=0.5)
        axs[idx].legend(loc='upper left', fontsize=5)
    
    st.pyplot(fig)

    # if True: # 
    # #    plt.figure(figsize=(5,3))
    #    rows = (totalItems // 2) + totalItems % 2
    #    fig, axIndefined = plt.subplots(nrows=rows,ncols=2,layout='constrained')
    #    if (totalItems % 2) == 1 :
    #     axIndefined[-1,-1].axis('off')

    #    for line in range(rows):
    #        axs.append(axIndefined[line][0])
    #    for line in range(rows):
    #        axs.append(axIndefined[line][1])
    #    plt.gcf().set_size_inches(10, 8)     
    
    # for idx, coly in enumerate(columnPlot):
    #      old = selConNameManyDataset(coly, checkBoxList2,dfList2,options2)
    #      new = selConNameManyDataset(coly, checkBoxList3,dfList3,options2)
    #      axs[idx].tick_params(labelsize=5)
    #      axs[idx].set_title(coly,fontsize=10)
    #      axs[idx].grid(True)
    #      axs[idx].hist(old,bins= 50, alpha=0.5, label="Old",color="y")
    #      axs[idx].hist(new,bins= 50, alpha=0.5, label="New",color="r")
    #      axs[idx].legend(loc='upper left', fontsize=5)

    # st.pyplot(fig)
    #print(columnChoose)


#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#
# with tab3:    
#     if histogram:
#         #x,y = selConName("Time",options,dfList[0])
#         old = selConNameManyDataset(options, checkBoxList2,dfList2, options)
#         new = selConNameManyDataset(options, checkBoxList3,dfList3, options)

#         #y = dfList[0] + dfList[1]
#         print (len(old),len(new))
#         bins = np.linspace(0, 20, 100)
        
#         fig, axOne = plt.subplots(nrows=1, ncols=1,layout='constrained', figsize=(8,5))
#         if len(new)!=0:
#             axOne.hist(new, alpha=0.5, label="New",color="y")
#         if len(old)!=0:
#             axOne.hist(old, alpha=0.5, label="Old",color="r")
#         axOne.grid(True)
#         axOne.set_title(options,fontsize=10)
#         #axOne.hist(y, bins, alpha=0.5, label='y')
#         axOne.legend(loc='upper right')
#         #plt.hist().set_size_inches(10, 8) 

#         st.pyplot(fig)

#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#
with tab3:
    pass
    # col6,col7 = st.columns(2)
    
    # with col6:
    # uploaded_files4 = st.file_uploader("Choose your file",type=['csv'])
        # for uploaded_file in uploaded_files4:
#            arquiveList4.append(uploaded_file.name)
    # df = read_csv(uploaded_file,sep=";")
    # df.rename(columns={"Time [s]": "Time"}, inplace= True)
    # incluiCondicaoTrabalho(df)
            # dfList4.append(df)
    # st.session_state['df'] = df
    # print(df)
    # with col7:
    #     options3 = st.selectbox('state',shortColumnsNames())
    #     for i in range(len(arquiveList4)):
    #         nomeArquivo = f"arquivo {i+1}"
    #         checkBoxList4.append(st.checkbox(nomeArquivo,False)) 
    #     with st.container():
    #     # if plot_fixed_mult:
    #         idSelected = []
    #         eixoAxs=[]
    #         plt.figure(figsize=(20,18))
    #         for idx,checkB in enumerate(checkBoxList4):
    #             if checkB:
    #                 idSelected.append(idx)

# totalItems = (len(idSelected))

    # corr_matrix = df.corr()
    # Criar um mapa de calor para visualizar a matriz de correlação
    # plt.figure(figsize=(10,8))
    # sns.heatmap(corr_matrix, annot=True, fmt=".2f")
    # plt.title('Matriz de Correlação')
    # plt.show()








