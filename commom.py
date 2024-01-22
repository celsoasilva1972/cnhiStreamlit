def commomHeader(st) :
    # §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
    #### titulo

    st.title ('Projeto Cana de Açúcar')
    # §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
    # imagem web

    st.image('https://storage.googleapis.com/images-cultivar/c297cae0-31f1-4478-a654-3911220ef4f3.jpeg',use_column_width=True)

    # §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
    # Campos de dados CNHI
    expander = st.expander("***_Descrição Parâmetros_***")

    expander.write ("A = Time = Tempo em segundos")
    expander.write ("B = ChopperRPM = Rotação do picador")
    expander.write ("C = ChopperHydPrs = Pressão hidraulica na bomba do picador")
    expander.write ("D = BHF = Indicativo da máquina estar colhendo ou não(circuito industrial)")
    expander.write ("E = BaseCutRPM = Velocidade do cortador de base")
    expander.write ("F = BaseCutHght = Altura do cortador de base  = adimensional 0~400")
    expander.write ("G = BaseCutPrs = Pressão do cortador de base ()")
    expander.write ("I = EngRPM = Rotação do motor")
    expander.write ("J = Js_1YAxPositn = Posição joystick")
    expander.write ("K = Js_1XAxPositn = Posição joystick")
    expander.write ("L = EngLoad = % Carga do motor (por ter reserva de torque pode chegar até 110%)")
    expander.write ("M = A2000_ChopperHydOilPrsHi = Alarme de pressão alta no picador")
    expander.write ("N = ChopperPctSetp = % Relação entre rotação do picador e rotação dos rolos(toletes maiores ou menores 10~25cm)")
    expander.write ("O = HydrostatChrgPrs = Progressão de carga em pascal ou psi (indicativo de algum problema hidraulico ou bomba)")



def showAllColumns(df, xColumnName, columnChoose, someColors, plt):
    contador = 0
    plt.figure(figsize=(20,10))
    fig, ax = plt.subplots()
    for coly in columnChoose:
        xValues, yValues = selConName(xColumnName,coly,df)
        ax.plot(xValues, yValues,color=someColors[contador], label=coly)
        contador += 1
    #ax.legend()
    #ax.xlabel(xColumnName);
    #ax.ylabel('Values');
    #ax.title('ALL SINALS') 
    st.pyplot(fig)
    print(columnChoose)
