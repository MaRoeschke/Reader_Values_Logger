import pandas as pd
import os
import numpy as np
from datetime import datetime


now = datetime.now()

def _open_trnsys(filepath):
    root, extension = os.path.splitext(filepath)
    if extension == ".xlsx":
        df_trnsys = pd.read_excel(filepath)
    elif extension == ".csv":
        df_trnsys = pd.read_csv(filepath, decimal=".", delimiter=",")
    else:
        print("File Error")


    # Erstellen des Dataframe trnsys
    trnsys_time2 = "Leistungen"
    Q_WP = "Q_cond"
    Schalter_WP_HZG = "S_WP_Hzg"
    Schalter_WP_TWE = "S_WP_TWE"
    Schalter_WP_K = "S_WP_Kuehl"

    df_trnsys = df_trnsys[[trnsys_time2, Q_WP, Schalter_WP_HZG, Schalter_WP_TWE, Schalter_WP_K]]
    df_trnsys.columns = ["Time2", "Q_WP [W]", "Heizen", "TWE", "Kuehlen"]
    df_trnsys[["Heizen", "TWE", "Kuehlen"]] = df_trnsys[["Heizen", "TWE", "Kuehlen"]].shift(1)
    df_trnsys[["Heizen", "TWE", "Kuehlen"]] = df_trnsys[["Heizen", "TWE", "Kuehlen"]].replace(np.nan, 0)

    #Wenn ein Schalter aktiv, dann Standby ungleich 0
    df_trnsys["Standby"] = df_trnsys["Heizen"] + df_trnsys["TWE"] + df_trnsys["Kuehlen"]

    print(now.strftime("%m/%d/%Y, %H:%M:%S") + str(": values_trnsys successfully load"))

    return df_trnsys