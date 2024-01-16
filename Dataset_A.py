import streamlit as st
import pandas as pd
import numpy as np
import plotly as plt
from pandas import read_csv

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# configurações da página
st.set_page_config(layout="wide",page_title="Cana de Açucar",page_icon="chart_with_upwards_trend")

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# funções

def incluiCondicaoTrabalhoOld(dfOrigin):
    condicao1 = [(dfOrigin['BHF'] == 1) & (dfOrigin['BaseCutHght'] <= 330) & (dfOrigin['GndSpd'] != 0) & (dfOrigin['EngRPM'] != 0)]
    opcoes1 = [1]
    dfOrigin["Working"] = np.select(condicao1, opcoes1,)

    condicao2 = [
    (dfOrigin['BHF']== 1) & (dfOrigin['GndSpd'] != 0) & (dfOrigin['EngRPM'] == 0)] 
    opcoes2 = [1]
    dfOrigin["Runing"] = np.select(condicao2, opcoes2, )

    condicao3 = [
    ((dfOrigin['BHF']== 1) |(dfOrigin['BHF']== 0)) & (dfOrigin['GndSpd'] == 0)] 
    opcoes3 = [1]
    dfOrigin["stoped"] = np.select(condicao3, opcoes3, )     


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

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
#### titulo

st.title ('Projeto Cana de açucar')
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# imagem web

st.image('https://storage.googleapis.com/images-cultivar/c297cae0-31f1-4478-a654-3911220ef4f3.jpeg',width=1080)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Campos de dados CNHI

st.write ("A = Time = Tempo em segundos")
st.write ("B = ChopperRPM = Rotação do picador")
st.write ("C = ChopperHydPrs = Pressão hidraulica na bomba do picador")
st.write ("D = BHF = Indicativo da máquina estar colhendo ou não(circuito industrial)")
st.write ("E = BaseCutRPM = Velocidade do cortador de base")
st.write ("F = BaseCutHght = Altura do cortador de base  = adimensional 0~400")
st.write ("G = BaseCutPrs = Pressão do cortador de base ()")
st.write ("H = GndSpd = Velocidade de deslocamento (km/h)")
st.write ("I = EngRPM = Rotação do motor")
st.write ("J = Js_1YAxPositn = Posição joystick")
st.write ("K = Js_1XAxPositn = Posição joystick")
st.write ("L = EngLoad = % Carga do motor (por ter reserva de torque pode chegar até 110%)")
st.write ("M = A2000_ChopperHydOilPrsHi = Alarme de pressão alta no picador")
st.write ("N = ChopperPctSetp = % Relação entre rotação do picador e rotação dos rolos(toletes maiores ou menores 10~25cm)")
st.write ("O = HydrostatChrgPrs = Progressão de carga em pascal ou psi (indicativo de algum problema hidraulico ou bomba)")

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

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Separação da página por Colunas

col1,col2 = st.columns(2)

with col1:
    arquivo = st.file_uploader("Escolha um arquivo CSV",type=['csv'])

    if arquivo:
        print(arquivo.type)
        match arquivo.type.split('/'):
            case 'text','csv':
                df = read_csv(arquivo,sep =";")
                            
                df.dtypes[df.dtypes == 'int64'] 

                df.replace(np.nan,0,inplace=True)
                
                df.rename(columns={"Time [s]": "Time"}, inplace= True)
                dfOrigin=df.copy()

                incluiCondicaoTrabalho(dfOrigin)               
                
#                df=(df-df.mean())/df.std()
                if normalizadoCheckbox:
                    df=(df-df.min())/(df.max()-df.min())
                    df["Time"]=dfOrigin["Time"]

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Gráfico de linhas com varíáveis específicas do dataset normalizado pelo Tempo
                if linechart_select:
                    st.subheader("Line Chart Select")
                    st.line_chart(df,x="Time",y=options)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Gráfico de linhas com todas as novas varíáveis específicas de trabalho pelo Tempo
                if linechart_Origin:
                    st.subheader("Line Chart Origin")
                    st.line_chart(dfOrigin,x="Time",y=Trabalho)

            
    else:
        st.error('Arquivo ainda não foi importado')            
        
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Tabela do DataFrame
with col2:
    if w1:
        st.dataframe(dfOrigin,width=2000,height=550)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Gráfico de linhas com todas as varíáveis pelo Tempo

if linechart_full:
	st.subheader("Line Chart Full")
	st.line_chart(df)

