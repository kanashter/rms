import csv
import pylab
import glob
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime, date, timedelta
from collections import Counter
from pandas.plotting import register_matplotlib_converters
from tqdm import tqdm, tqdm_notebook
register_matplotlib_converters()

class rms:
    def data_merge(y):
        path = str(str(y) + '/data')
        extension = 'csv'
        all_files = glob.glob(path + '/*.csv')
        li = []
        for filename in all_files:
            df = pd.read_csv(filename, index_col = None, header = 0, low_memory = False)
            li.append(df)
            frame = pd.concat(li, axis = 0, ignore_index = True)
        all_dates = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for date in all_dates:
            frame['Date Made'] = frame['Date Made'].map(lambda x: x.lstrip(date))
            frame['Arrive Date'] = frame['Arrive Date'].map(lambda x: x.lstrip(date))
            frame['Depart Date'] = frame['Depart Date'].map(lambda x: x.lstrip(date))
        frame.to_csv(y + '.csv', index = False)

    def data_process(y):
        data = pd.read_csv(y + '.csv', low_memory = False)
        cols = data.columns
        cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, (str)) else x)
        data.columns = cols
        data['Date_Made'] = pd.to_datetime(data['Date_Made'], format = ' %d %b %Y %H:%M %p')
        data['Arrive_Date'] = pd.to_datetime(pd.to_datetime(data['Arrive_Date'], format = ' %d %b %Y %H:%M %p').dt.strftime('%Y-%m-%d'))
        data['Depart_Date'] = pd.to_datetime(pd.to_datetime(data['Depart_Date'], format = ' %d %b %Y %H:%M %p').dt.strftime('%Y-%m-%d'))
        try:
            if y == 'liberty':
                data = data[data['Date_Made'] >= pd.to_datetime('2017-9-15')]
                data = data[data['Room_Type'] != 'Car Parking (CP) - Liberty']
            elif y == 'manners':
                data = data[data['Date_Made'] >= pd.to_datetime('2017-9-15')]
                data = data[data['Room_Type'] != 'Car Park - The Setup on Manners']
            elif y == 'dixon':
                data = data[data['Date_Made'] >= pd.to_datetime('2018-1-15')]
            elif y == 'laneway':
                data = data[data['Date_Made'] >= pd.to_datetime('2019-4-1')]
        except ValueError:
            print('No Valid Property Provided, please enter \'liberty\', \'manners\', \'dixon\', \'laneway\'')
        data['counter'] = 1
        return data

    def created_bookings(x, y):
        start = pd.to_datetime(date.today() - timedelta(days=30))
        frame = y
        name = str(x)
        frame.index = frame['Date_Made']
        file = str(x.lower()) + '/export/Bookings Created - ' + str(x) + '.csv'
        image =  str(x.lower()) + '/export/Bookings Created - ' + str(x)
        resampled_frame = frame.resample('D').counter.sum()
        fig = plt.figure(figsize=(30, 10))
        plt.plot(resampled_frame.loc[start:], color = 'k', label = 'Bookings Made')
        plt.plot(resampled_frame.loc[start:].rolling(7, center=True).mean(), color = 'r', linestyle = ':', label = 'Trend')
        plt.title('Bookings Created at ' + str(name))
        plt.xticks(rotation = '45')
        plt.grid('x')
        plt.legend()
        plt.savefig(image)
        plt.show()
        resampled_frame.to_csv(file)
        return resampled_frame

    def occupancy_figures(x, y):
        start = pd.to_datetime(date.today() - timedelta(days=30))
        end = pd.to_datetime(date.today() + timedelta(days=30))
        frame = y
        name = str(x)
        frame.index = frame['Arrive_Date']
        file = str(x.lower()) + '/export/Occupancy - ' + str(x) + '.csv'
        image = str(x.lower()) + '/export/Occupancy - ' + str(x)
        if x.lower() == 'liberty':
            room_number = 43
        elif x.lower() == 'manners':
            room_number = 81
        elif x.lower() == 'dixon':
            room_number = 67
        elif x.lower() == 'laneway':
            room_number = 62
        c = Counter(frame['Arrive_Date'])
        c = sorted(c.items())
        arrivals = [i[0] for i in c]
        arrival_freq = [i[1] for i in c]
        z = Counter(frame['Depart_Date'])
        z = sorted(z.items())
        departures = [i[0] for i in z]
        depart_freq = [i[1] for i in z]
        arrivals_df = pd.DataFrame(arrival_freq, arrivals)
        departures_df = pd.DataFrame(depart_freq, departures)
        arrivals_df.columns=['Arrive_Date']
        departures_df.columns=['Depart_Date']
        arrivals_departures = arrivals_df.join(departures_df, how = 'outer')
        arrivals_departures = arrivals_departures.fillna(0)
        arrivals_departures['Daily_Occupied'] = (arrivals_departures['Arrive_Date'] - arrivals_departures['Depart_Date'])
        arrivals_departures['In_House'] = arrivals_departures['Daily_Occupied'].cumsum()
        arrivals_departures['Occupancy'] = ((arrivals_departures['In_House'])/room_number)
        fig = plt.figure(figsize=(30, 10))
        plt.plot((arrivals_departures.loc[start:end].Occupancy)*100, color = 'k', label = 'Occupancy')
        plt.plot((arrivals_departures.loc[start:end].Occupancy.rolling(7, center = True).mean())*100,
                    color = 'r', linestyle = ':', label = 'Trend')
        plt.axvline(pd.to_datetime(date.today()), color = 'c', linestyle = ':', label = 'Current Date')
        plt.title('Occupancy - ' + str(name))
        plt.xticks(rotation='45')
        plt.grid('x')
        plt.legend()
        plt.savefig(image)
        plt.show()
        arrivals_departures.to_csv(file)
        return arrivals_departures

    def revenue_totals(x, y):
        start = pd.to_datetime(date.today() - timedelta(days=30))
        frame = y
        name = str(x)
        frame.name = name
        frame.index = frame['Date_Made']
        file = str(x.lower()) + '/export/Revenue - ' + str(x) + '.csv'
        image = str(x.lower()) + '/export/Revenue - ' + str(x)
        frame_resample = frame.resample('D').Tariff.sum()
        fig = plt.figure(figsize=(30, 10))
        plt.plot(frame_resample.loc[start:], color = 'k', label = 'Total Sale Value')
        plt.plot(frame_resample.loc[start:].rolling(7, center = True).mean(), color = 'r', linestyle = ':', label = 'Trend')
        plt.title('Revenue Per Day (Total Sale Value) - ' + str(name))
        plt.xticks(rotation='45')
        plt.grid('x')
        plt.legend()
        plt.savefig(image)
        plt.show()
        frame_resample.to_csv(file)

    def revenue_add(x, y):
        scratch = pd.DataFrame()
        sample_date_range = pd.date_range(x['Arrive_Date'], freq='D', periods = x['Nights'])
        scratch['Date'] = sample_date_range
        scratch['Revenue'] = x['Daily_Tariff']
        temp = pd.DataFrame()
        temp['Date'] = pd.date_range('2017-01-01', periods = 1500, freq = '1D')
        temp['Revenue'] = 0
        scratch2 = pd.merge(temp, scratch, on='Date', how='left').fillna(0)
        scratch2['Revenue'] = scratch2['Revenue_y']
        temp2 = scratch2.drop(['Revenue_x', 'Revenue_y'], axis=1)
        y['temp'] = temp2['Revenue']
        y['Revenue'] = y['temp'] + y['Revenue']
        y.drop(['temp'], axis = 1)

    def cashflow(x, y):
        start = pd.to_datetime(date.today() - timedelta(days=30))
        end = pd.to_datetime(date.today() + timedelta(days=30))
        frame = y
        file = str(x.lower()) + '/export/Cashflow - ' + str(x) + '.csv'
        image = str(x.lower()) + '/export/Cashflow - ' + str(x)
        name = str(x)
        frame['Nights'] = (frame['Depart_Date'] - frame['Arrive_Date']).dt.days
        frame = frame[frame['Nights'] >= 0]

        special = pd.DataFrame()
        special['Date'] = pd.date_range('2017-01-01', periods = 1500, freq = '1D')
        special['Revenue'] = 0.0

        with tqdm(total=len(list(frame.iterrows())), desc='Working - ' + str(name)) as pbar:
            for index, x in frame.iterrows():
                rms.revenue_add(x, special)
                pbar.update(1)

        special.index = special['Date']
        special.index.name = None
        special.drop(['Date', 'temp'], inplace= True, axis = 1)

        fig = plt.figure(figsize=(30,10))
        plt.plot(special.loc[start:end].Revenue, color = 'k', label = 'Cashflow')
        plt.plot(special.Revenue.loc[start:end].rolling(7, center = True).mean(), color = 'r', linestyle = ':', label = 'Trend')
        plt.title('Cashflow - ' + str(name))
        plt.xticks(rotation='45')
        plt.grid('x')
        plt.legend()
        plt.savefig(image)
        plt.show()
        special.to_csv(file)

        return special
