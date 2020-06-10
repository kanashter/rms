# WMGNZ RMS Data Analysis

## Function file and basic workflow sheet to deliver basic KPI's


#### Table of contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Function List](#function-list)
5. [The Work File](#the-work-file)
6. [Suggested future actions](#suggested-future-actions)

### Introduction
The following scripts are designed to take information from the RMS based properties in the WMGNZ portfolio.<br>These scripts are run in an [Anaconda](https://anaconda.org), [Python 3](https://python.org) environment.
For a full list of environment requirements please refer to the [requirements file](requirements.txt).

### Installation

The base requirements are as follows
- [Anaconda](https://anaconda.org)
- [Atom](https://atom.io)
- [Hydrogen](https://atom.io/packages/hydrogen) addon
- Windows based system

Extract al files and folder from the releases page, and set up and new anaconda environment based on the [requirements.txt](requirements.txt) file.
Activate your newly installed anaconda environment - and open the rms folder as a new project in Atom.

### Usage

The flowchart for using this script is as follows
> 1. [RMS](https://app.rmscloud.com/Login)
> 2. Date Made/Modified
> 3. Set dates to 2017-1-1 -> Current Date
> 4. Download individual properties, and save resulting .csv to the \<property\>/data folder
> 5. - Activate Anaconda environment, open rms as project folder, run [work.py](work.py)
>    - Or run work.py from an Anaconda active command line interface.
> 6. Create a full database snapshot using the [database_create](database_create.py) file.

This will produce graphs and dataframes for four key KPI's
- Bookings created per days
- Occupancy per day
- Total Value of sale per day
- Cashflow per day

### Function list

Inside the [rms](rms.py) file are a number of functions designed to produce these dataframes. These functions are listed below.

__Function__ | __Description__
-|-
data_merge(\<property\>)|Combines all .csv files within the <property>/data folder. This allows for multiple files to be placed in the various folders. Exports these combined files to a single sorted .csv in the rms folder
data_process(\<property\>)|Takes the file created by data_merge and produces a workable dataframe. All datetimes are converted to datetime objects, spaces in column names are replaced with an '_' character to allow for easier coding.<br> (i.e. liberty.Date_Made)
created_bookings(\<Property Name)\>, \<property dataframe\>)|Takes the property and resamples the number of bookings created per day. Returns this resampled dataframe for further actions if required. Provides a graphical representation of the last 30 days of bookings.
occupancy_figures(\<Property Name)\>, \<property dataframe\>)|Returns a dataframe of the number of arrivals and departures per day, with a daily movement, total in house and occupancy figures included. Please note - all property room numbers are fixed, alterations require modifications to the [rms](rms.py) file. <br>Returns a graph of the previous 30 days, and upcoming 30 days occupancy to help predict trends.
revenue_totals(\<Property Name)\>, \<property dataframe\>)|Returns a dataframe of the total value of each sale created per day. (Please note, for long term bookings this may not be a helpful metric, though ADR can be calculated by combining the total with the number of nights sold).<br>Returns a graphical representation of the previous 30 days.
cashflow(\<Property Name)\>, \<property dataframe\>)|Alternate to the revenue_totals function, this function calculates the amount of revenue spent per day per person and collates each booking to an individual dateline, before merging all together. <br>As this function runs on each individual line, this can take ~5-10 minutes to complete depending on the speed of your device. Progress is tracked. <br> Files and images are saved.
revenue_add(\<x, y\>)|Auxiliary function to the cashflow function - does not need to be modified.

These are the base level functions designed to return dataframes. All saved files are placed in the relevant \<property\>/export folder.

### The Work File

The work file produces the basic KPI dataframes required for tracking. The following dataframes are produced
- \<property\> &rarr; Full property DataFrame
- \<property\>_created &rarr; Resampled created DataFrame
- \<property\>_occ &rarr; Movement sheet DataFrame
- \<property\>_total &rarr; Resampled Total Spend DataFrame
- \<property\>_cashflow &rarr; Resampled cashflow DataFrame

Further operations can be performed on these DataFrames.

### Suggested Future Actions
[prophet](prophet.py) is an example of fb_prophet that can be used to statistically predicted various factors.<br>[Tensorflow](https://www.tensorflow.org/) is another framework this project may function well with.

## Licensing
All files incuded are licensed under the MIT Open Source license, which can be found [here](license.md). For any questions please feel free to get in touch.
