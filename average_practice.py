import numpy as np
import pandas as pd
import scipy as sp
import csvkit

df = pd.read_csv('test_set.csv')
#df = df.dropna()
#count the number of non NA values in each row for flagging rows that have too many NAs, defined as less than 5
df['count'] = df.count(axis=1)

mon = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
#create dictionary with months as keys and the average energy usage as values
months = {}
for i in mon:
    months[i] = (np.average(df[i].dropna()))

#create the new columns that keep track of how customer deviates from the average each month
mon_diff = []
for i in mon:
    df[i+'_avgdiff'] = (months[i] - df[i])/months[i]
    mon_diff.append(i+'_avgdiff')

#calculate the average of the customer deviations
    df['deviation'] = np.nanmean(df[mon_diff],axis=1)

#for each NA in the original data, fill it in as the monthly average +/- the average deviation of the customer
for i in mon:
    df[i] = df[i].fillna(months[i]+(months[i]*df['deviation']))

q75, q25 = np.percentile(df['jan'], [75 ,25])
iqr = q75 - q25
print iqr
upper_outlier = iqr + (1.5*iqr)
lower_outlier = iqr - (1.5*iqr)
print upper_outlier
print lower_outlier
