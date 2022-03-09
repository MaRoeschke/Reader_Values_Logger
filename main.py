import pandas as pd
import datetime
import tkinter as tk
import sys

from tkinter import filedialog

from Tools.open_values_logger import _open_logger
from Tools.open_values_trnsys import _open_trnsys
from Tools.create_date_column import _create_date
from Tools.energie_assignment import _assign_energies
from Tools.create_day_values import _create_days

start_time = datetime.datetime.strptime("01 01 00 00", '%m %d %H %M')

#Einlesen des Gebäudeenergiebedarfes aus values_logger:
controll_logger = False                     #Controllstruktur für richtiges File
while controll_logger is False:
    root = tk.Tk()
    root.withdraw()
    file_path_logger = filedialog.askopenfilename()
    if file_path_logger.find("logger") != -1:
        controll_logger = True

#Einlesen der Energiewert Energieerzeugungssystem aus values_trnsys:
controll_trnsys = False                     #Controllstruktur für richtiges File
while controll_trnsys is False:
    root = tk.Tk()
    root.withdraw()
    file_path_trnsys = filedialog.askopenfilename()
    if file_path_trnsys.find("trnsys") != -1:
        controll_trnsys = True

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

print(df_values_day)
