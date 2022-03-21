import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

now = datetime.now()

def _create_plots(df_typtage, path):
    #Aufteilen der Daten in drei Saisons
    mask1 = df_typtage['Cluster/FaktorT'].str.contains('C4/') | df_typtage['Cluster/FaktorT'].str.contains('C5/') | \
            df_typtage['Cluster/FaktorT'].str.contains('C3/')
    plot1 = df_typtage[mask1]
    mask2 = df_typtage['Cluster/FaktorT'].str.contains('C42/') | df_typtage['Cluster/FaktorT'].str.contains('C32/') | \
            df_typtage['Cluster/FaktorT'].str.contains('C43/')
    plot2 = df_typtage[mask2]
    mask3 = df_typtage['Cluster/FaktorT'].str.contains('C33/') | df_typtage['Cluster/FaktorT'].str.contains('C22/') | \
            df_typtage['Cluster/FaktorT'].str.contains('C44/')
    plot3 = df_typtage[mask3]

    df_plots = [plot1, plot2, plot3]

    #Pfade für Test
    #path1 = 'C:/Users/Eckert/Desktop/plot1.csv'
    #path2 = 'C:/Users/Eckert/Desktop/plot2.csv'
    #path3 = 'C:/Users/Eckert/Desktop/plot3.csv'
    #all_path = [path1, path2, path3]
    #save_path = r'C:\Users\Eckert\Desktop\Variation Typtagebestimmung\pythonProject1\PNG'


    #Array mit Farben für Darstellung Balkendiagramm
    red_array=['#750000','#930000','#AE0000','#CE0000','#EA0000','#FF0000','#FF2D2D','#FF5151','#ff7575','#FF9797','#FFB5B5','#FFD2D2','#FFECEC']
    blue_array=['#000079','#000093','#0000C6','#0000E3','#2828FF','#4A4AFF','#6A6AFF','#7D7DFF','#9393FF','#AAAAFF','#B9B9FF','#CECEFF','#DDDDFF','#ECECFF','#FBFBFF']
    green_array=['#006000','#007500','#009100','#00A600','#00BB00','#00DB00','#00EC00','#28FF28','#53FF53','#79FF79','#93FF93','#A6FFA6','#BBFFBB','#CEFFCE','#DFFFDF','#F0FFF0']
    color_array=[red_array,blue_array, green_array]

    #Clustervarianten
    cluster_var = [["C4", 'C3', 'C5'],['C42', 'C32', 'C43'],['C44','C33','C22']]

    #Array für Diagrammtitel nach Einteilung in Saisons
    saison = ["Ganzjährig", "Saison heizlastig", "Saison gleich"]

    #Array mit notwendigen Wertespalten
    heads = [['W_PV [kWh/a]', 'Q_H [kWh/a]','Q_K [kWh/a]'],
             [ 'Q_WP_H [kWh/a]', 'Q_WP_K [kWh/a]', 'Q_WP_TWE [kWh/a]'],
             [ 'JAZ', 'SEER']]

    #Array für Diagrammüberschriften
    titles = ['Gebäudedaten: Vergleich Typtage und Jahressimulation', 'therm. Energie Wärmepumpe: Vergleich Typtage und Jahressimulation', 'JAZ und SEER: Vergleich Typtage und Jahressimulation']

    #Schleife für Saisons
    for i in range(len(df_plots)):

        df_plot = df_plots[i]
        #Auswahl der Spalten mit rel.Abweichung und Erstellung eines neuen Dataframes für Auswertung
        mask = df_plot['Cluster Nr.'] == 3
        df_plot = df_plot[mask]

        #Spalten runden

        df_plot['W_PV [kWh/a]'].astype(float).round(2)


    #Aufteilung in die Varianten der Typtagvariation
        variante = df_plot["Cluster/FaktorT"].str.split("/", n=1, expand=True)
        variante.columns = ["Cluster", "Faktor"]
        df_var = variante["Cluster"]
        df_plot = df_plot.assign(Cluster = df_var)
        #gleich Typtagergebnisse entfernen
        df_plot1 = df_plot.drop_duplicates(subset=["Cluster","W_PV [kWh/a]"])

        #Farben zuweisen
        color_plot = []
        labels = np.array(df_plot1["Cluster/FaktorT"])
        c1 = df_plot1[df_plot1["Cluster"] == cluster_var[i][0]].count()['Cluster']
        for k in range(0,(c1)):
            color_plot.append(color_array[0][k])
        c2 = df_plot1[df_plot1["Cluster"] == cluster_var[i][1]].count()['Cluster']
        for k in range(0, (c2)):
            color_plot.append(color_array[1][k])
        c3 = df_plot1[df_plot1["Cluster"] == cluster_var[i][2]].count()['Cluster']
        for k in range(0, (c3)):
            color_plot.append(color_array[2][k])

     #Schleife für jede Typtagvariante
        for j in range(0,3):                                            #Für 3er Diagramm
            if len(heads[j]) == 3:
                x = np.array(df_plot1[heads[j][0]])
                y = np.array(df_plot1[heads[j][1]])
                z = np.array(df_plot1[heads[j][2]])

                X = np.arange(len(x))
                Y = np.arange(len(y))
                Z = np.arange(len(z))

                fig = plt.figure(j+1)
                gs = fig.add_gridspec(1, 3, wspace=0)                   #Anordnung Subplots
                axs = gs.subplots( sharex=True, sharey=True)            #Gemeinsame Achsen der Subplots

                title = titles[j] + str("(") + saison[i] + str(")")     #Zusammensetzen der Diagrammtitel
                fig.suptitle(title)
                axs[0].bar(X, x, color=color_plot)
                axs[0].set_title(heads[j][0])
                axs[0].get_xaxis().set_visible(False)
                axs[0].grid(axis='y')

                axs[1].bar(Y, y, color=color_plot)
                axs[1].set_title(heads[j][1])
                axs[1].get_xaxis().set_visible(False)
                axs[1].grid(axis='y')

                axs[2].bar(Z, z, color=color_plot)
                axs[2].set_title(heads[j][2])
                axs[2].get_xaxis().set_visible(False)
                axs[2].grid(axis='y')

                #Erstellen der Legende
                keys = labels
                values = color_plot
                colors = dict(zip(keys, values))                        #Dictonary aus Wert und Farbe
                labels = list(colors.keys())
                handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
                plt.legend(handles, labels, loc='lower center', bbox_to_anchor=(-0.5, -0.5),
                           fancybox=True, ncol=4
                           )

                fig.supylabel('rel. Abweichung [%]')

                #Speichern als .png
                savein = path
                name = str("\\Abb.") + str(i+1) + str(j+1) + str(".png")
                plt.savefig(savein + name, bbox_inches='tight', dpi=200)

            elif len(heads[j]) == 2:                                    #Für 2er Diagramm
                x = np.array(df_plot1[heads[j][0]])
                y = np.array(df_plot1[heads[j][1]])

                X = np.arange(len(x))
                Y = np.arange(len(y))

                fig = plt.figure(j + 1)
                gs = fig.add_gridspec(1, 2, wspace=0)
                axs = gs.subplots(sharex=True, sharey=True)

                title = titles[j] + str("(") + saison[i] + str(")")
                fig.suptitle(title)

                axs[0].bar(X, x, color=color_plot, label=labels)
                axs[0].set_title(heads[j][0])
                axs[0].get_xaxis().set_visible(False)
                axs[0].grid(axis='y')

                axs[1].bar(Y, y, color=color_plot, label=labels)
                axs[1].set_title(heads[j][1])
                axs[1].get_xaxis().set_visible(False)
                axs[1].grid(axis='y')

                keys = labels
                values = color_plot
                colors = dict(zip(keys, values))
                labels = list(colors.keys())
                handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
                plt.legend(handles, labels, loc='lower center',bbox_to_anchor=(0,-0.5),
                           fancybox=True, ncol=4
                           )
                fig.supylabel('rel. Abweichung [%]')
                savein = path
                name = str("\\Abb.") + str(i + 1) + str(j + 1) + str(".png")
                plt.savefig(savein + name, bbox_inches='tight', dpi=200)

    print(now.strftime("%m/%d/%Y, %H:%M:%S") + str(": Plots erstellt"))






