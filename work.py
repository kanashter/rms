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

#%% -- Created Bookings
liberty_created = rms.created_bookings('Liberty', liberty)
manners_created = rms.created_bookings('Manners', manners)
dixon_created = rms.created_bookings('Dixon', dixon)
laneway_created = rms.created_bookings('Laneway', laneway)

#%% -- Create Occupancy Dataframes and Graphs
liberty_occ = rms.occupancy_figures('Liberty', liberty)
manners_occ = rms.occupancy_figures('Manners', manners)
dixon_occ = rms.occupancy_figures('Dixon', dixon)
laneway_occ = rms.occupancy_figures('Laneway', laneway)

#%% -- Total Sales (Revenue of Total Sale)
liberty_total = rms.revenue_totals('Liberty', liberty)
manners_total = rms.revenue_totals('Manners', manners)
dixon_total = rms.revenue_totals('Dixon', dixon)
laneway_total = rms.revenue_totals('Laneway', laneway)

#%% -- Cashflow Values (Takes daily spend of each guest)
liberty_cashflow = rms.cashflow('Liberty', liberty)
manners_cashflow = rms.cashflow('Manners', manners)
dixon_cashflow = rms.cashflow('Dixon', dixon)
laneway_cashflow = rms.cashflow('Laneway', laneway)
