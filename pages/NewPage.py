import streamlit as st
import pandas as pd
import numpy as np
from pandas import read_csv
from commom import commomHeader
import plotly as plt
import matplotlib.pyplot as plt

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #

st.set_page_config(layout="wide",page_title="Cana de Açucar",page_icon="chart_with_upwards_trend")

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Variáveis

arquiveList = [] # nome do arquivo
dfList = [] # dataFrame de cada arquivo
checkBoxList = [] # todos os checkbox


def columnsNames():
    columns =  ['ChopperRPM','ChopperHydPrs','BHF','BaseCutRPM','BaseCutHght','BaseCutPrs','GndSpd','EngRPM','Js_1YAxPositn','Js_1XAxPositn','EngLoad','A2000_ChopperHydOilPrsHi','ChopperPctSetp','HydrostatChrgPrs']
    return columns

options = st.sidebar.selectbox(
    'Linechart_select Y variable',
    columnsNames())

plot_fixed_mult=st.sidebar.checkbox("Plot Estático Multilinhas",False)


def selConName(colx, coly,df):
    df_filter = df.loc[:, [colx, coly]]
    df_filter.dropna(inplace = True)
    #print(df_filter.head())
    return df_filter[colx], df_filter[coly]


#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True,type=['csv'])
for uploaded_file in uploaded_files:
    arquiveList.append(uploaded_file.name)
    df = read_csv(uploaded_file,sep=";")
    df.rename(columns={"Time [s]": "Time"}, inplace= True)
    dfList.append(df)

if len (dfList) != 0:

    for i in range(len(arquiveList)):
        nomeArquivo = f"arquivo {i+1}"
        checkBoxList.append(st.sidebar.checkbox(nomeArquivo,False)) 


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













