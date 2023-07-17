#!/usr/bin/python3

import time
import datetime
import numpy as np
import pandas as pd

CUT_OFF = np.arange(1, 101)

dt = pd.read_excel('raw_data.xlsx')
dt['DayOfYear'] = dt['FlightDate'].dt.dayofyear

old_close = np.round(sum(dt.Sale_Flag.values) * 100 / dt.shape[0], 1)
print("Initial close ratio = {}".format(old_close))

def assign_groups(dates, cut_off):
  """ Assign group values depending on difference between dates (14 days)"""
  diff_l   = []
  groups_l = []

  i_group  = 1

  if len(dates) == 1:
    groups_l.append(1)
    diff_l.append(0)
  else:
    groups_l.append(1)
    diff_l.append(0)
    for i in range(1, len(dates)):
      diff_days = dates[i] - dates[i - 1]
      if diff_days <= cut_off:
        groups_l.append(i_group)
      else:
        i_group += 1
        groups_l.append(i_group)
      diff_l.append(diff_days)
  return diff_l, groups_l

def add_groups_dt(usr, cut_off):
  """Add group values to user specific dataframe"""
  dates = usr.DayOfYear.values
  differences, groups = assign_groups(dates, cut_off)
  usr['Diffs']  = differences
  usr['Groups'] = groups
  return usr

def find_quotes(usr):
  """Find quotes that match the requirements in each group"""
  unique_groups = np.unique(usr.Groups.values)
  quotes_list   = []

  for i in unique_groups:
    tmp = usr.loc[usr.Groups == i]
    if 1 in np.unique(tmp.Sale_Flag):
      quotes = tmp.loc[tmp.Sale_Flag == 1, 'QuoteID'].values.tolist()
    else:
      quotes = tmp.loc[(tmp.Sale_Flag == 0) & (tmp.QuoteCreationDateTime == tmp.\
                                               QuoteCreationDateTime.max()),\
                       'QuoteID'].values.tolist()
    quotes_list.extend(quotes)
  return quotes_list

def iterate_users(dt, usr, cut_off):
  """Filter data to user and return quotes"""
  usr_dt = dt.loc[dt.UserID == usr]
  usr_dt = usr_dt.sort_values(by = 'FlightDate')
  usr_dt = add_groups_dt(usr_dt, cut_off)
  usr_quotes = find_quotes(usr_dt)
  return usr_quotes

def compute_new_close(dt, cut_off):
  users = np.unique(dt.UserID.values)
  good_quotes = []
  for u in users:
    user_quotes = iterate_users(dt, u, cut_off)
    good_quotes.extend(user_quotes)
  new_dt = dt.loc[dt.QuoteID.isin(good_quotes)]
  new_dt = new_dt.drop(['DayOfYear'], axis = 1)
  new_close = np.round(sum(new_dt.Sale_Flag.values) * 100 / new_dt.shape[0], 1)
  if cut_off % 5 == 0:
    print("Cut off = {} new mean close ratio = {}".format(cut_off, new_close))
  return cut_off, new_close


def main():
  """Filter to 1 user, deduplicate quotes, compute new ratio, save output """
  cut_offs     = []
  close_ratios = []
  
  for day in CUT_OFF:
    local_cut, local_close = compute_new_close(dt, day)
    cut_offs.append(local_cut)
    close_ratios.append(local_close)
  
  pd.DataFrame({'cut_off': cut_offs, 'new_ratio': close_ratios}).to_csv('new_close_ratios.csv')
  

if __name__ == '__main__':
  start_time = time.time()
  main()
  end_time = time.time()
  duration = end_time - start_time
  print("\nRuntime for this program was {} seconds.".format(duration))
