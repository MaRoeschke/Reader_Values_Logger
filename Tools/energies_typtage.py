import pandas as pd
import numpy as np

#File der Clustervarianten, wobei Varianten durch Schlüssel z.B. C42/T1 (C=4Tage Heiz-/2Tage-Kühlperiode und T1 = Temperaturfaktor=1,0) gekennzeichnet sind
filepath = "Files/Typtagvariation_TRY2015_524042130202_Jahr.csv"

def determine_energy_typtage(df_energies):
# Einlesen der Typtagvarianten
    df_typtage = pd.read_csv(filepath, decimal=",", delimiter=";")
    df_typtage[["Cluster Nr.", "Tag Nr.","direkte Str.", "diffuse Str.", "Windgeschw."]] = df_typtage[["Cluster Nr.", "Tag Nr.","direkte Str.", "diffuse Str.", "Windgeschw."]].astype(int)
#Initialisierung eines leeren Dataframe in dem die Energiewert den Clustertagen zugeordnet werden
    df_new = pd.DataFrame(columns = ["MM","DD","ta [°C]","W_PV [W]","Q_TWW [W]","Q_H [W]", "Q_K [W]", "W_WP_TWE [W]", "Q_WP_TWE [W]", "Q_WP_H [W]", "Q_WP_K [W]", "W_WP_H1 [W]", "W_WP_K1 [W]"]
    )
    for i in range(len(df_typtage)):
        day = (df_typtage["Tag Nr."].iloc[i])                               # Auswahl des Tages aus den Clustern
        df_new.loc[i] = df_energies.loc[day - 1]                            # Zuodnung des Ernergiewerte zum Clustertag
    df_merge = pd.concat([df_typtage,df_new], axis=1, sort=False)           # Zusammenführen Dataframe Cluster und Energiewerte
    df_merge1 = df_merge.drop(labels=['MM','DD','ta [°C]',], axis=1)

#Initialisierung eines leeren Dataframe für Vergleich Jahreswerte aus jahressimulation und Clustering
#Für eine bessere Auswertung wird die AusgabeCSV in der nächsten Schleife vorbereitet,dabei wird Tabelle in Dataframe erstellt
    df_year = pd.DataFrame(columns=['Ergebnis', 'W_PV [kWh/a]', 'Q_H [kWh/a]', 'Q_TWW [kWh/a]', 'Q_K [kWh/a]', 'W_WP_H [kWh/a]', 'W_WP_K [kWh/a]', 'W_WP_TWE [kWh/a]', 'Q_WP_H [kWh/a]', 'Q_WP_K [kWh/a]', 'Q_WP_TWE [kWh/a]', 'JAZ', 'SEER'])
#Einmalige Berechnung der Jahreswerte aus Jahressimulation
    wpv = df_energies["W_PV [W]"].sum() / 1000
    qh = df_energies["Q_H [W]"].sum() / 1000
    qtww = df_energies["Q_TWW [W]"].sum() / 1000
    qk = df_energies["Q_K [W]"].sum() / 1000
    wwph = df_energies["W_WP_H1 [W]"].sum() / 1000
    wwpk = df_energies["W_WP_K1 [W]"].sum() / 1000
    wwpt = df_energies["W_WP_TWE [W]"].sum() / 1000
    qwph = df_energies["Q_WP_H [W]"].sum() / 1000
    qwpk = df_energies["Q_WP_K [W]"].sum() / 1000
    qwpt = df_energies["Q_WP_TWE [W]"].sum() / 1000

    for i in range(len(df_merge1)):

        #Wenn Clustertag Nr.1, dann jede Spalte = Spalte Tagesenergiewert * Anzahl Tage im Cluster
        if df_merge1['Cluster Nr.'].loc[i] == 1:
            j = i                                               #Laufvariable für 1 Zeil der Variante
            df_year.loc[i,'Ergebnis'] = "Summe Clustering"      #Beschriftung innere Tabelle
            df_year.loc[i,'W_PV [kWh/a]'] = df_merge1['Anzahl Tage'].loc[i] * df_merge1["W_PV [W]"].loc[i] /1000
            df_year.loc[i,'Q_H [kWh/a]'] =  df_merge1['Anzahl Tage'].loc[i] * df_merge1["Q_H [W]"].loc[i] / 1000
            df_year.loc[i,'Q_TWW [kWh/a]'] = df_merge1['Anzahl Tage'].loc[i] * df_merge1["Q_TWW [W]"].loc[i] / 1000
            df_year.loc[i,'Q_K [kWh/a]'] = df_merge1['Anzahl Tage'].loc[i] * df_merge1["Q_K [W]"].loc[i] / 1000
            df_year.loc[i,'W_WP_H [kWh/a]'] = df_merge1['Anzahl Tage'].loc[i] * df_merge1["W_WP_H1 [W]"].loc[i] / 1000
            df_year.loc[i,'W_WP_K [kWh/a]'] = df_merge1['Anzahl Tage'].loc[i] * df_merge1["W_WP_K1 [W]"].loc[i] / 1000
            df_year.loc[i,'W_WP_TWE [kWh/a]'] = df_merge1['Anzahl Tage'].loc[i] * df_merge1["W_WP_TWE [W]"].loc[i] / 1000
            df_year.loc[i,'Q_WP_H [kWh/a]'] = df_merge1['Anzahl Tage'].loc[i] * df_merge1["Q_WP_H [W]"].loc[i] / 1000
            df_year.loc[i,'Q_WP_K [kWh/a]'] = df_merge1['Anzahl Tage'].loc[i] * df_merge1["Q_WP_K [W]"].loc[i] / 1000
            df_year.loc[i,'Q_WP_TWE [kWh/a]'] = df_merge1['Anzahl Tage'].loc[i] * df_merge1["Q_WP_TWE [W]"].loc[i] / 1000
        #Wenn Clustertag Nr. 2, dann Einfügen der Jahreswerte aus Jahressimulation,
        #Nachfolgen Energiewerte Clustertag 2 * Anzahl Tage in Cluster Nr. 2 auf Clustertag Nr.1 Addieren
        elif df_merge1['Cluster Nr.'].loc[i] == 2:
            df_year.loc[i,'Ergebnis'] = "Summe Simulation"      #Beschriftung innerer Tabelle
            df_year.loc[i, 'W_PV [kWh/a]'] = wpv
            df_year.loc[i, 'Q_H [kWh/a]'] = qh
            df_year.loc[i, 'Q_TWW [kWh/a]'] = qtww
            df_year.loc[i, 'Q_K [kWh/a]'] = qk
            df_year.loc[i, 'W_WP_H [kWh/a]'] = wwph
            df_year.loc[i, 'W_WP_K [kWh/a]'] = wwpk
            df_year.loc[i, 'W_WP_TWE [kWh/a]'] = wwpt
            df_year.loc[i, 'Q_WP_H [kWh/a]'] = qwph
            df_year.loc[i, 'Q_WP_K [kWh/a]'] = qwpk
            df_year.loc[i, 'Q_WP_TWE [kWh/a]'] = qwpt

            df_year.loc[j, 'W_PV [kWh/a]'] = df_year.loc[j, 'W_PV [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * \
                                             df_merge1["W_PV [W]"].loc[i] / 1000
            df_year.loc[j, 'Q_H [kWh/a]'] = df_year.loc[j, 'Q_H [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * \
                                            df_merge1["Q_H [W]"].loc[i] / 1000
            df_year.loc[j, 'Q_TWW [kWh/a]'] = df_year.loc[j, 'Q_TWW [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * \
                                              df_merge1["Q_TWW [W]"].loc[i] / 1000
            df_year.loc[j, 'Q_K [kWh/a]'] = df_year.loc[j, 'Q_K [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * \
                                            df_merge1["Q_K [W]"].loc[i] / 1000
            df_year.loc[j, 'W_WP_H [kWh/a]'] = df_year.loc[j, 'W_WP_H [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * \
                                               df_merge1["W_WP_H1 [W]"].loc[i] / 1000
            df_year.loc[j, 'W_WP_K [kWh/a]'] = df_year.loc[j, 'W_WP_K [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * \
                                               df_merge1["W_WP_K1 [W]"].loc[i] / 1000
            df_year.loc[j, 'W_WP_TWE [kWh/a]'] = df_year.loc[j, 'W_WP_TWE [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * \
                                                 df_merge1["W_WP_TWE [W]"].loc[i] / 1000
            df_year.loc[j, 'Q_WP_H [kWh/a]'] = df_year.loc[j, 'Q_WP_H [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * \
                                               df_merge1["Q_WP_H [W]"].loc[i] / 1000
            df_year.loc[j, 'Q_WP_K [kWh/a]'] = df_year.loc[j, 'Q_WP_K [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * \
                                               df_merge1["Q_WP_K [W]"].loc[i] / 1000
            df_year.loc[j, 'Q_WP_TWE [kWh/a]'] = df_year.loc[j, 'Q_WP_TWE [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * \
                                                 df_merge1["Q_WP_TWE [W]"].loc[i] / 1000


        # Innere Tabelle für Variante zuende, daher
        #  Energiewerte Clustertag n * Anzahl Tage in Cluster Nr. n auf Clustertag Nr.1 Addieren
        else:
            df_year.loc[i, 'Ergebnis'] = "---"
            df_year.loc[j, 'W_PV [kWh/a]'] = df_year.loc[j, 'W_PV [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * df_merge1["W_PV [W]"].loc[i] / 1000
            df_year.loc[j, 'Q_H [kWh/a]'] = df_year.loc[j, 'Q_H [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * df_merge1["Q_H [W]"].loc[i] / 1000
            df_year.loc[j, 'Q_TWW [kWh/a]'] = df_year.loc[j, 'Q_TWW [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * df_merge1["Q_TWW [W]"].loc[i] / 1000
            df_year.loc[j, 'Q_K [kWh/a]'] = df_year.loc[j, 'Q_K [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * df_merge1["Q_K [W]"].loc[i] / 1000
            df_year.loc[j, 'W_WP_H [kWh/a]'] = df_year.loc[j, 'W_WP_H [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * df_merge1["W_WP_H1 [W]"].loc[i] / 1000
            df_year.loc[j, 'W_WP_K [kWh/a]'] = df_year.loc[j, 'W_WP_K [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * df_merge1["W_WP_K1 [W]"].loc[i] / 1000
            df_year.loc[j, 'W_WP_TWE [kWh/a]'] = df_year.loc[j, 'W_WP_TWE [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * df_merge1["W_WP_TWE [W]"].loc[i] / 1000
            df_year.loc[j, 'Q_WP_H [kWh/a]'] = df_year.loc[j, 'Q_WP_H [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * df_merge1["Q_WP_H [W]"].loc[i] / 1000
            df_year.loc[j, 'Q_WP_K [kWh/a]'] = df_year.loc[j, 'Q_WP_K [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * df_merge1["Q_WP_K [W]"].loc[i] / 1000
            df_year.loc[j, 'Q_WP_TWE [kWh/a]'] = df_year.loc[j, 'Q_WP_TWE [kWh/a]'] + df_merge1['Anzahl Tage'].loc[i] * df_merge1["Q_WP_TWE [W]"].loc[i] / 1000

    for i in range(len(df_merge1)):

        # Wenn Clustertag Nr.1
        if df_merge1['Cluster Nr.'].loc[i] == 1:
            j = i  # Laufvariable für 1 Zeil der Variante
            # JAZ Clustering
            df_year.loc[i, 'JAZ'] = (df_year.loc[i, 'Q_WP_H [kWh/a]'] + df_year.loc[i, 'Q_WP_TWE [kWh/a]']) / (df_year.loc[i, 'W_WP_H [kWh/a]'] + df_year.loc[i, 'W_WP_TWE [kWh/a]'])
            # SEER Clustering
            if df_year.loc[i, 'W_WP_K [kWh/a]'] != 0:
                df_year.loc[i, 'SEER'] = df_year.loc[i, 'Q_WP_K [kWh/a]'] / df_year.loc[i, 'W_WP_K [kWh/a]']
            else:
                df_year.loc[i, 'SEER'] = 0
        elif df_merge1['Cluster Nr.'].loc[i] == 2:
            # JAZ Simulation
            df_year.loc[i, 'JAZ'] = (df_year.loc[i, 'Q_WP_H [kWh/a]'] + df_year.loc[i, 'Q_WP_TWE [kWh/a]']) / (
                        df_year.loc[i, 'W_WP_H [kWh/a]'] + df_year.loc[i, 'W_WP_TWE [kWh/a]'])
            # SEER Simulation
            df_year.loc[i, 'SEER'] = df_year.loc[i, 'Q_WP_K [kWh/a]'] / df_year.loc[i, 'W_WP_K [kWh/a]']

        # Wenn Clustertag Nr. 3, Berechnung rel.Abweichung

        elif df_merge1['Cluster Nr.'].loc[i] == 3:
            df_year.loc[i, 'Ergebnis'] = "rel.Abweichung"       #Beschriftung innerer Tabelle
            df_year.loc[i, 'W_PV [kWh/a]'] = ((df_year.loc[i-2, 'W_PV [kWh/a]'] - df_year.loc[i-1, 'W_PV [kWh/a]'])*100) / df_year.loc[i-1, 'W_PV [kWh/a]']
            df_year.loc[i, 'Q_H [kWh/a]'] = (df_year.loc[i-2, 'Q_H [kWh/a]'] - df_year.loc[i-1, 'Q_H [kWh/a]'])*100 / df_year.loc[i-1, 'Q_H [kWh/a]']
            df_year.loc[i, 'Q_TWW [kWh/a]'] = (df_year.loc[i-2, 'Q_TWW [kWh/a]'] - df_year.loc[i-1, 'Q_TWW [kWh/a]'])*100 / df_year.loc[i-1, 'Q_TWW [kWh/a]']
            df_year.loc[i, 'Q_K [kWh/a]'] = (df_year.loc[i-2, 'Q_K [kWh/a]'] - df_year.loc[i-1, 'Q_K [kWh/a]'])*100 / df_year.loc[i-1, 'Q_K [kWh/a]']
            df_year.loc[i, 'W_WP_H [kWh/a]'] = (df_year.loc[i-2, 'W_WP_H [kWh/a]'] - df_year.loc[i-1, 'W_WP_H [kWh/a]'])*100 / df_year.loc[i-1, 'W_WP_H [kWh/a]']
            df_year.loc[i, 'W_WP_K [kWh/a]'] = (df_year.loc[i-2, 'W_WP_K [kWh/a]'] - df_year.loc[i-1, 'W_WP_K [kWh/a]'])*100 / df_year.loc[i-1, 'W_WP_K [kWh/a]']
            df_year.loc[i, 'W_WP_TWE [kWh/a]'] = (df_year.loc[i-2, 'W_WP_TWE [kWh/a]'] - df_year.loc[i-1, 'W_WP_TWE [kWh/a]'])*100 / df_year.loc[i-1, 'W_WP_TWE [kWh/a]']
            df_year.loc[i, 'Q_WP_H [kWh/a]'] = (df_year.loc[i-2, 'Q_WP_H [kWh/a]'] - df_year.loc[i-1, 'Q_WP_H [kWh/a]'])*100 / df_year.loc[i-1, 'Q_WP_H [kWh/a]']
            df_year.loc[i, 'Q_WP_K [kWh/a]'] = (df_year.loc[i-2, 'Q_WP_K [kWh/a]'] - df_year.loc[i-1, 'Q_WP_K [kWh/a]'])*100 / df_year.loc[i-1, 'Q_WP_K [kWh/a]']
            df_year.loc[i, 'Q_WP_TWE [kWh/a]'] = (df_year.loc[i-2, 'Q_WP_TWE [kWh/a]'] - df_year.loc[i-1, 'Q_WP_TWE [kWh/a]'])*100 / df_year.loc[i-1, 'Q_WP_TWE [kWh/a]']
            df_year[['W_PV [kWh/a]', 'Q_H [kWh/a]', 'Q_TWW [kWh/a]', 'Q_K [kWh/a]', 'W_WP_H [kWh/a]', 'W_WP_K [kWh/a]',
                     'W_WP_TWE [kWh/a]', 'Q_WP_H [kWh/a]', 'Q_WP_K [kWh/a]', 'Q_WP_TWE [kWh/a]']]= np.round(df_year[['W_PV [kWh/a]','Q_H [kWh/a]','Q_TWW [kWh/a]','Q_K [kWh/a]', 'W_WP_H [kWh/a]', 'W_WP_K [kWh/a]', 'W_WP_TWE [kWh/a]', 'Q_WP_H [kWh/a]', 'Q_WP_K [kWh/a]', 'Q_WP_TWE [kWh/a]']], decimals=2)

            df_year.loc[i, 'JAZ'] = ((df_year.loc[i-2, 'JAZ'] - df_year.loc[i-1, 'JAZ'])*100) / df_year.loc[i-1, 'JAZ']
            df_year.loc[i, 'SEER'] = ((df_year.loc[i - 2, 'SEER'] - df_year.loc[i - 1, 'SEER']) * 100) / df_year.loc[i - 1, 'SEER']
    df_final = pd.concat([df_merge1, df_year], axis=1, sort=False)

    #Berechnung JAZ und SEER





    return df_final