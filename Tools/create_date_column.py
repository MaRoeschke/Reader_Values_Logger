import pandas as pd
import datetime


def _create_date(df, start_time):
    kuehlperiode_anfang = datetime.datetime.strptime("05 01 00 00", "%m %d %H %M")
    kuehlperiode_ende = datetime.datetime.strptime("09 30 23 59", "%m %d %H %M")
    date = []
    kuehlperiode = []

    for ind in df.index:
        split_date = []

        next_date = start_time + datetime.timedelta(minutes=ind)
        split_date = [next_date.month, next_date.day, next_date.hour, next_date.minute]
        date.append(split_date)
        if next_date > kuehlperiode_anfang and next_date < kuehlperiode_ende:
            kuehlperiode.append(1)
        else:
            kuehlperiode.append(0)
    df_date = pd.DataFrame(date, columns=[["MM", "DD", "HH", "MN"]])
    df_status = pd.DataFrame(kuehlperiode, columns=["kuehlen"])
    df_with_date = pd.concat([df_date, df_status, df], axis=1, sort=False)

    return df_with_date