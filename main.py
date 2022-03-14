import pandas as pd
import datetime
import tkinter as tk
import os

from tkinter import filedialog

from Tools.open_values_logger import _open_logger
from Tools.open_values_trnsys import _open_trnsys
from Tools.create_date_column import _create_date
from Tools.energie_assignment import _assign_energies
from Tools.create_day_values import _create_days
from Tools.energies_typtage import determine_energy_typtage

start_time = datetime.datetime.strptime("01 01 00 00", '%m %d %H %M')
dev = True
file_path_logger = "Files/2021-11-22_values_logger ohne BAT(csv).csv"
file_path_trnsys = "Files/2021-11-22_values_trnsys ohne BAT(CSV).csv"

while dev is True:
    #Einlesen des Gebäudeenergiebedarfes aus values_logger:
    controll_logger = False                     #Controllstruktur für richtiges File
    while controll_logger is False:
        root = tk.Tk()
        root.withdraw()
        file_path_logger = filedialog.askopenfilename()
        if file_path_logger.find("logger") != -1:
            controll_logger = True
            ordnerpfad = os.path.dirname(file_path_logger)

    #Einlesen der Energiewert Energieerzeugungssystem aus values_trnsys:
    controll_trnsys = False                     #Controllstruktur für richtiges File
    while controll_trnsys is False:
        root = tk.Tk()
        root.withdraw()
        file_path_trnsys = filedialog.askopenfilename()
        if file_path_trnsys.find("trnsys") != -1 and ordnerpfad == os.path.dirname(file_path_trnsys):
            controll_trnsys = True
    break
#Öffnen der Datei values_logger und Rückgabe Dataframe
df_logger = _open_logger(file_path_logger)

#Öfnnen der Datei values_trnsys und Rückgabe Dataframe
df_trnsys = _open_trnsys(file_path_trnsys)

#Dataframes zusammenführen
df = pd.concat([df_logger, df_trnsys], axis=1, sort=False)

#Erstellen der Datumsspalten
df1 = _create_date(df, start_time)
df_complete = _assign_energies(df1)
df_values_day = _create_days(df_complete)


#Einlesen der Typtagvariation
df_typtage = determine_energy_typtage(df_values_day)

#Ergebnisse Speichern

#Neuen Ordner erstellen
index = 0
control = False
folder = 'Results_TRY_Analyse'


while control is False:
    if index == 0:
        path = os.path.join(ordnerpfad, folder).replace("\\","/")
    else:
        path = os.path.join(ordnerpfad, folder1).replace("\\", "/")
    if not os.path.exists(path):
        os.mkdir(path)
        control = True
    else:
        index = index + 1
        folder1 = folder + "(" + str(index) + ")"
#Dateiname
file_name_results = os.path.splitext(os.path.basename(file_path_logger))[0]
file_name_results = file_name_results.split("_")[0]
file_name_results = "results_Try_Analyse_" + str(file_name_results) + ".csv"
path_results = os.path.join(path,file_name_results).replace("\\","/")
df_typtage.to_csv(path_results)

