import pandas as pd
import numpy as np

def _assign_energies(df):
# Energie bei Status TWE zu TWE
    df["W_WP_TWE [W]"] = np.where(df["TWE"] == 1, df["W_WP [W]"], 0)
    df["Q_WP_TWE [W]"] = np.where(df["TWE"] == 1, df["Q_WP [W]"], 0)
# Energie bei Status Heizen zu Heizenergie
    df["W_WP_H [W]"] = np.where(df["Heizen"] == 1, df["W_WP [W]"], 0)
    df["Q_WP_H [W]"] = np.where(df["Heizen"] == 1, df["Q_WP [W]"], 0)
# Energie bei Status Kühlen zu Kühlenergie
    df["W_WP_K [W]"] = np.where(df["Kuehlen"] == 1, df["W_WP [W]"], 0)
    df["Q_WP_K [W]"] = np.where(df["Kuehlen"] == 1, df["Q_WP [W]"], 0)
# Wenn kein Status aktiv, dann Elektroenergie zu Standby
    df["W_Standby [W]"] = np.where(df["Standby"] == 0, df["W_WP [W]"], 0)

# Negativ definierte Wärmeenergie zu positiv
    df["Q_WP_H [W]"] = df["Q_WP_H [W]"] * (-1)
    df["Q_WP_TWE [W]"] = df["Q_WP_TWE [W]"] * (-1)

# Wenn nicht Kühlperiode, dann Elektroenergie fürs Heizen = Heizenergie + Standbyenergie
    df["W_WP_H1 [W]"] = np.where(df["Kuehlen"] == 0, df["W_WP_H [W]"] + df["W_Standby [W]"],
                                    df["W_WP_H [W]"])
# Wenn Kühlperiode, dann Elektroenergie fürs Kühlen = Kühlenergie + Standbyenergie
    df["W_WP_K1 [W]"] = np.where(df["Kuehlen"] == 1, df["W_WP_K [W]"] + df["W_Standby [W]"],
                                    df["W_WP_K [W]"])

    df["Energy"] = np.where(df["Q_WP [W]"] < 0, df["Q_WP [W]"] * (-1), df["Q_WP [W]"])
#alte Spalten entfernen und Spaltennamen festlegen
    df = df.drop(
        labels=['kuehlen', 'Time2', 'Q_WP [W]', 'W_WP [W]', 'W_Standby [W]', 'Energy', 'Heizen', 'TWE',
                'Standby', 'W_WP_H [W]', 'W_WP_K [W]', 'Kuehlen'], axis=1)
    df.columns = ["MM", "DD", "HH", "MN", "Time", "ta [°C]", "W_PV [W]", "Q_TWW [W]", "Q_H [W]", "Q_K [W]",
                     "W_WP_TWE [W]", "Q_WP_TWE [W]", "Q_WP_H [W]", "Q_WP_K [W]", "W_WP_H1 [W]", "W_WP_K1 [W]"]

    temperatur = df[["MM", "DD", "HH", "MN", "ta [°C]"]]
    temperatur_min = temperatur.groupby(["MM", "DD", "HH"], as_index=False).min()
    temperatur_max = temperatur.groupby(["MM", "DD", "HH"], as_index=False).max()
    temperatur_min1 = temperatur_min.groupby(["MM", "DD"], as_index=False).min()
    temperatur_max1 = temperatur_max.groupby(["MM", "DD"], as_index=False).max()

    return df