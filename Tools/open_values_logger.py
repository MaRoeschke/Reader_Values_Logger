import pandas as pd
import os
from datetime import datetime

now = datetime.now()

def _open_logger(filepath):
    root, extension = os.path.splitext(filepath)
    if extension == ".xlsx":
        df_logger = pd.read_excel(filepath)
    elif extension == ".csv":
        df_logger = pd.read_csv(filepath, decimal=".", delimiter=",")
    else:
        print("File Error")

#Erstellen des Dataframe logger
    #Spaltennamen
    trnsys_time = "MQTT/T207/SENDEN/Input207_3"
    t_a = "MQTT/T207/SENDEN/Input207_7"
    pv_leistung = "MQTT/T207/SENDEN/Input207_5"
    heizlast = "MQTT/T207/SENDEN/Input207_18"
    tww_last = "MQTT/T207/SENDEN/Input207_19"
    W_WP = "MQTT/T207/SENDEN/Input207_6"

    df_logger = df_logger[[trnsys_time, t_a, pv_leistung, heizlast, tww_last, W_WP]]
    df_logger.columns = ["Time", "ta [°C]", "W_PV [W]", "Q_H1 [W]", "Q_TWW", "W_WP [W]"]

    #Dataframe für Heizwärmebedarf (Werte > 0)
    df_heizlast = df_logger.loc[:, ["Q_H1 [W]"]]
    df_heizlast = df_heizlast.clip(lower=0)

    #Dataframe für Kühlenergiebedarf (Werte <0)
    df_kuehllast = df_logger.loc[:, ["Q_H1 [W]"]]
    df_kuehllast = df_kuehllast.clip(upper=0)
    df_kuehllast.columns = ['Q_K [W]']
    df_heizlast.columns = ['Q_H [W]']

    df_logger = df_logger.drop(labels=["Q_H1 [W]"], axis=1)
    df_logger["Q_H [W]"] = df_heizlast["Q_H [W]"]
    df_logger["Q_K [W]"] = df_kuehllast['Q_K [W]']

    print(now.strftime("%m/%d/%Y, %H:%M:%S") + (": values_logger_successfully load"))

    return df_logger