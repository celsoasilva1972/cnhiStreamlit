
def renameColumns(df):
    df.rename(columns={"Time [s]": "Time"}, inplace= True)
    df.rename(columns={"PB_Ucm2_Status_84::BHF_On_Off": "BHF"}, inplace= True)
    df.rename(columns={"Hydstat_Charge_Press": "HydrostatChrgPrs"}, inplace= True)