
def renameColumns(df):
    df.rename(columns={"Time [s]": "Time"}, inplace= True)
    df.rename(columns={"PB_Ucm2_Status_84::BHF_On_Off": "BHF"}, inplace= True)
    df.rename(columns={"Hydstat_Charge_Press" : "HydrostatChrgPrs"}, inplace= True)
    ## files from 2024season
    df.rename(columns={"Time increment [sec]": "Time"}, inplace= True)
    df.rename(columns={"Chopper_Rpm" : "ChopperRPM"}, inplace= True)
    df.rename(columns={"Chopper_Hydr_Press" : "ChopperHydPrs"}, inplace= True)
    df.rename(columns={"BHF_On_Off" : "BHF"}, inplace= True)
    ## onde está o 'BaseCutRPM'?                       
    df.rename(columns={"Prim_Extr_Rpm_Setp":"BaseCutRPM"}, inplace= True) #colocado qualquer rpm para testar
                       
    df.rename(columns={"basecutter_height":"BaseCutHght"}, inplace= True)
    df.rename(columns={"Basecutter_pressure":"BaseCutPrs"}, inplace= True)
    df.rename(columns={"Ground_Speed":"GndSpd"}, inplace= True)
    df.rename(columns={"Engine_Rpm":"EngRPM"}, inplace= True)
    df.rename(columns={"y_position":"Js_1YAxPositn"}, inplace= True)
    df.rename(columns={"x_position":"Js_1XAxPositn"}, inplace= True)
    df.rename(columns={"Eng_Load":"EngLoad"}, inplace= True)
    df.rename(columns={"A2000_Chopper_Hydr_Oil_Press_High":"A2000_ChopperHydOilPrsHi"}, inplace= True)
    df.rename(columns={"Chopper_Pct_Setp":"ChopperPctSetp"}, inplace= True)