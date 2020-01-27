import datetime
import json
from ast import literal_eval

import requests
import matplotlib.pyplot as plt
import pandas as pd

from data import traindata
from data_model import TrainAnnouncement


def runner():
    active_trains, _ = business_rules_converter()
    adv_time = list((i.adv_time[0:10] for i in active_trains))
    delays = list((i.delay_in_mins for i in active_trains))
    adv_time = list((datetime.datetime.fromisoformat(i) for i in adv_time))
    legacy_dataframe = pd.DataFrame({'Date': adv_time, 'Delay': delays}, columns=['Date', 'Delay'])
    legacy_dataframe.Date = pd.to_datetime(legacy_dataframe.Date)
    legacy_dataframe.set_index('Date', inplace=True)

    # Iterera lists
    i = 0
    avg_delays = {}
    for xx in adv_time:
        if xx in avg_delays:
            avg_delays[xx]['vals'].append(delays[i])
        else:
            avg_delays[xx] = {'vals': [delays[i]]}
        i += 1
    minutes = []
    v = {}
    for values in avg_delays.values():
        minutes.append(sum(values['vals']) / len(values['vals']))
    for key in avg_delays.keys():
        values = avg_delays[key]
        timestamp_string = key.strftime("%Y-%m-%d   ")
        v[timestamp_string] = sum(values['vals']) / len(values['vals'])

    legacy_dataframe.sort_index()

    data = {'minutes': list(v.values()),
            'datum': list(v.keys())}
    df = pd.DataFrame(data)

    df.plot(kind='bar', x='datum', y='minutes')
    '''df1 = df1.groupby([df1['Datum'].dt.date])['Delay'].mean()
    print(df1)
    plt.figure()
    df1.plot.hist(alpha=0.5)
    plt.show()'''

    plt.xlabel("Time")
    plt.ylabel("Avg deelay in mins")
    plt.title("Avg rain delays in minutes at Stockholm Central")
    plt.show()


def data_gathering():
    headers = {"content-type": "text/xml"}

    XML = (
        '<REQUEST><LOGIN authenticationkey="your_hardcoded_api_key" />'
        '<QUERY objecttype="TrainAnnouncement" schemaversion="1.3" orderby="AdvertisedTimeAtLocation">'
        "<FILTER>"
        "<AND>"
        '<EQ name="ActivityType" value="Avgang" />'
        '<EQ name="LocationSignature" value="Sto" />'
        "<OR>"
        "<AND>"
        '<GT name="AdvertisedTimeAtLocation" value="$dateadd(-30.00:00)" />'
        '<LT name="AdvertisedTimeAtLocation" value="$dateadd(14:00:00)" />'
        "</AND>"
        "</OR>"
        "</AND>"
        "</FILTER>"
        "<INCLUDE>AdvertisedTrainIdent</INCLUDE>"
        "<INCLUDE>AdvertisedTimeAtLocation</INCLUDE>"
        "<INCLUDE>TimeAtLocation</INCLUDE>"
        "<INCLUDE>ToLocation</INCLUDE>"
        "<INCLUDE>Canceled</INCLUDE>"
        "<INCLUDE>Deviation</INCLUDE>"
        "</QUERY>"
        "</REQUEST>"
    )

    r = requests.post(
        url="https://api.trafikinfo.trafikverket.se/v2/data.json",
        data=XML,
        headers=headers,
    )
    return r.text


def business_rules_converter():
    lista = []
    # data = data_gathering()
    # data = data.replace("false", "False")
    data = traindata.train_data
    # data = literal_eval(data)
    d = data.get("RESPONSE").get("RESULT")[0].values()
    e = list(data.get("RESPONSE").get("RESULT")[0].values())[0]

    canceled_trains = []
    n = 0
    for i in e:
        if i.get("Canceled") != False:
            canceled_trains.append(i)
            e.pop(n)
            n = n + 1

    active_trains = []
    for i in e:
        if clean_data(i):
            active_trains.append(clean_data(i))

    for train_call in active_trains:
        nr = 0
        if train_call.est_time_location != None:
            start = datetime.datetime.fromisoformat(train_call.est_time_location)
            end = datetime.datetime.fromisoformat(train_call.adv_time)
            if start < end:
                nr = (end - start).seconds
        train_call.add_delay(nr / 60)
    return active_trains, canceled_trains


def clean_data(i):
    if i.get("Canceled") != True:
        trains_call = TrainAnnouncement(
            i["AdvertisedTimeAtLocation"],
            i["AdvertisedTrainIdent"],
            i["Canceled"],
            i.get("TimeAtLocation"),
        )
        return trains_call
    return None


runner()
