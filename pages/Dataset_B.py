import streamlit as st
import pandas as pd
from pandas import read_csv
from commom import commomHeader


# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
#configurações da página
st.set_page_config(layout="wide",page_title="Cana de Açucar",page_icon="chart_with_upwards_trend")


# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
#####Funções

# Lê arquivo CSV
def readFilePandasCsv(filename, separation):
    df=pd.read_csv(filename,sep=separation,index_col=False)
    return df

# Seleciona target e as demais colunas
def getXYColumns(df):
    colunas = df.columns
    x = colunas[0]
    y = colunas[1:]
    return x,y.tolist()

# Cria novo dataframe com o nome das colunas
def getNewDataframe(columnNamesList):
    newDf = pd.DataFrame(columns=columnNamesList)
    return newDf  

# Faz o recorte do dataframe
def recorteDf (df, colx, coly):
    SliceDf = df.loc[:, [colx, coly]]
    SliceDf.dropna(inplace = True)
    SliceDf['diff'] = SliceDf[colx].diff()
    SliceDf.drop(index=SliceDf.index[0], axis=0, inplace=True)
    return SliceDf

# Gera as estatisticas Média,Desvio Padrão e Frequência
def createStatistics(df, yName):
    listValues = []
    listValues.append(yName)
    listValues.append(df['diff'].mean().round(2))
    listValues.append(df['diff'].std())
    listValues.append(1/df['diff'].mean().round(2))
    listValues.append(df[yName].max())
    listValues.append(df[yName].min())

    return listValues

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
# Barra Lateral
w1 = st.sidebar.checkbox("show table", False)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Carregamento dos dados
arquivo = st.file_uploader("Escolha um arquivo CSV_B",type=['csv'])

if arquivo:
    print(arquivo.type)
    match arquivo.type.split('/'):
        case 'text','csv':
            df = read_csv(arquivo,sep =";")
            
            df.dtypes[df.dtypes == 'int64'] 
            df.rename(columns={"Time [s]": "Time"}, inplace= True)

else:
    st.error('Arquivo ainda não foi importado')
    df = pd.DataFrame(columns=['Time','ChopperRPM','ChopperHydPrs','BHF','BaseCutRPM','BaseCutHght','BaseCutPrs','GndSpd','EngRPM','Js_1YAxPositn','Js_1XAxPositn','EngLoad','A2000_ChopperHydOilPrsHi','ChopperPctSetp','HydrostatChrgPrs'])

x, Col_list  = getXYColumns(df)
colStatisticas = ['Colunas','Media','DesvioPadrao','Frequência','Maximo','Minimo']
statisticas = getNewDataframe(colStatisticas)
i = 0

if arquivo:
    for coly in Col_list:
        dfTwoColumns = recorteDf(df,x, coly)
        i += 1
        statisticas.loc[i] = createStatistics(dfTwoColumns, coly)

#Tabela do DataFrame
if w1:
    st.dataframe(statisticas,width=2000,height=550)



# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #