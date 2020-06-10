import pandas as pd
from rms import rms

#%% -- Merge data in all folders
all_files = ['liberty', 'manners', 'dixon', 'laneway']
for file in all_files:
    rms.data_merge(file)

#%% -- Get Dataframes
liberty = rms.data_process('liberty')
manners = rms.data_process('manners')
dixon = rms.data_process('dixon')
laneway = rms.data_process('laneway')

#%% -- Add specific named columns
liberty['property'] = 'Liberty Apartment Hotel'
manners['property'] = 'The Setup on Manners'
dixon['property'] = 'The Setup on Dixon'
laneway['property'] = 'Laneway Backpackers'

#%% -- Merge
targets = [liberty, manners, dixon, laneway]
merged = pd.concat(targets, ignore_index = True)

#%% -- save
merged.to_csv('rms_database.csv', index = False)
