#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import pymongo 
import pandas as pd
import numpy as np

jobs = pd.read_csv('data/stackoverflow_jobs.csv')

#
print "Read data " + str(len(jobs.index)) + " rows."


# Salary 
jobs.salary = jobs.salary.fillna('')

# creating a new column for equity
jobs['equity'] = jobs['salary'].str.contains('Provides Equity')

# striping out equity part 
salary = jobs.salary 
salary = jobs.salary.map(lambda x: x.replace("Provides Equity","").replace("/","").strip())

salary = salary.str.extract('(?P<currency>[^\d]*)(?P<number_low>[\d,]+) - (?P<number_high>[\d,]+$)')

salary.number_low = salary.number_low.fillna(0)
salary.number_high = salary.number_high.fillna(0)
salary.currency = salary.currency.fillna('')

# mapping the new columns back
jobs['currency'] = salary.currency
jobs['salary_low'] = salary.number_low
jobs['salary_high'] = salary.number_high

# Location

# filling for location missing 
jobs.location = jobs.location.fillna('') 
 
location_split = lambda x: pd.Series([i for i in x.split(',')])
locations = jobs['location'].apply(location_split)

locations.rename(columns={0:'city', 1: 'location_1', 2: 'location_2'},inplace=True)
     
# Fixing US States
us_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

locations['location_1'] = locations['location_1'].str.strip()
locations.loc[locations['location_1'].isin(us_states),'location_2'] = "US"

# if location_2 is null then location_1 column has the country 
# if location_2 is not null then location_2 has the country and location_1 contains the state 
jobs['country'] = np.where(locations['location_2'].isnull(), locations['location_1'], locations['location_2'])
jobs['state'] = np.where(locations['location_2'].notnull(), locations['location_1'], '')

jobs['city'] = locations['city']

# filling na for country 
jobs.country = jobs.country.fillna('')

# stripping spaces from new columns
jobs['city'] = jobs['city'].str.strip()
jobs['country'] = jobs['country'].str.strip()

# replacing some of the country names with their english version 
jobs.loc[jobs['country'].str.contains('Deutschland'),'country'] = 'Germany' # Deutschland -> Germany
jobs.loc[jobs['country'].str.contains('Österreich'),'country'] = 'Austria' # Österreich -> Austria
jobs.loc[jobs['country'].str.contains('Suisse'), 'country'] = 'Switzerland' # Suisse -> Switzerland
jobs.loc[jobs['country'].str.contains('Schweiz'), 'country'] = 'Switzerland' # Schweiz -> Switzerland
jobs.loc[jobs['country'].str.contains('Espagne'), 'country'] = 'Spain' # Espagne -> Spain
jobs.loc[jobs['country'].str.contains('Spanien'), 'country'] = 'Spain' # Spanien -> Spain
jobs.loc[jobs['country'].str.contains('République tchèque'), 'country'] = 'Czech Republic' # République tchèque -> Czech Republic
jobs.loc[jobs['country'].str.contains('Niederlande'), 'country'] = 'Netherlands' # Niederlande -> Netherlands
jobs.loc[jobs['country'].str.contains('Polen'), 'country'] = 'Poland' # Polen -> Poland
jobs.loc[jobs['country'].str.contains('Bulgarien'), 'country'] = 'Bulgaria' # Bulgarien -> Bulgaria
jobs.loc[jobs['country'].str.contains('Belgique'), 'country'] = 'Belgium' # Belgique -> Belgium
jobs.loc[jobs['country'].str.contains('Belgien'), 'country'] = 'Belgium' # Belgien -> Belgium
jobs.loc[jobs['country'].str.contains('Irland'), 'country'] = 'Ireland' # Irland -> Ireland
jobs.loc[jobs['country'].str.contains('Tschechische Republik'), 'country'] = 'Czech Republic' # Czech Republic
jobs.loc[jobs['country'].str.contains('Royaume-Uni'), 'country'] = 'UK' # UK
jobs.loc[jobs['country'].str.contains('Vereinigtes Königreich'), 'country'] = 'UK' # UK


# redefining columns
jobs.title = jobs.title.astype(str)
print "Writing out enhanced data " + str(len(jobs.index)) + " rows."

# saving the result to csv 
jobs.to_csv('data/stackoverflow_jobs_enhanced.csv', index = False)

