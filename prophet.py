import pandas as pd
from datetime import datetime, date, timedelta
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
from rms import rms

#%%
rms.data_merge('liberty')

#%% -- Get Dataframes
liberty = rms.data_process('liberty')

#%%
liberty_occ = rms.occupancy_figures('Liberty', liberty)

#%%
temp = liberty_occ.loc[:pd.to_datetime(date.today())]
prophet_df = pd.DataFrame()
prophet_df['ds'] = temp.index
prophet_df['y'] = (temp.In_House.values)

#%%
m = Prophet(seasonality_mode='multiplicative')
m.add_country_holidays(country_name='NZ')
m.fit(prophet_df)

#%%
future = m.make_future_dataframe(periods=90)
forecast = m.predict(future)

#%%
fig1 = m.plot(forecast, xlabel='Date', ylabel='In House', figsize=(20,10))

#%%
fig2 = m.plot_components(forecast, figsize=(20,20))
