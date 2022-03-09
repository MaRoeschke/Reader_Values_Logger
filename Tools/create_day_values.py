import pandas as pd

def _create_days(df):
    sumH = df["Q_WP_H [W]"].sum()
    sumT = df["Q_WP_TWE [W]"].sum()
    sumk = df["Q_WP_K [W]"].sum()
    WH = df["W_WP_H1 [W]"].sum()
    WT = df["W_WP_TWE [W]"].sum()
    Wk = df["W_WP_K1 [W]"].sum()
    W = WH + WT + Wk
    df1 = df.groupby(["MM", "DD", "HH"], as_index=False).sum()
    df1[["ta [°C]", "W_PV [W]", "Q_TWW [W]", "Q_H [W]", "Q_K [W]", "W_WP_TWE [W]", "Q_WP_TWE [W]", "Q_WP_H [W]",
           "Q_WP_K [W]", "W_WP_H1 [W]", "W_WP_K1 [W]"]] = df1[
                                                              ["ta [°C]", "W_PV [W]", "Q_TWW [W]", "Q_H [W]", "Q_K [W]",
                                                               "W_WP_TWE [W]", "Q_WP_TWE [W]", "Q_WP_H [W]",
                                                               "Q_WP_K [W]", "W_WP_H1 [W]", "W_WP_K1 [W]"]] / 60

    df2 = df1.drop(labels=['MN', 'Time'], axis=1)
    df3 = df2.groupby(["MM", "DD"], as_index=False).sum()
    df3["ta [°C]"] = df3["ta [°C]"] / 24
    df3 = df3.drop(labels=['HH'], axis=1)

    return df3