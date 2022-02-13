# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 11:40:38 2022

@author: momo8
"""

import pandas as pd
import numpy as np
import glassdoorscraper 

keyword = 'Data Scientist'
path = "C:/Users/momo8/Documents/ds_salary_proj/chromedriver.exe"
df = glassdoorscraper.glassdoorscraper(path,keyword,10000,30)
df = pd.DataFrame(df)
df.to_csv('glassdoor.csv')

df = pd.read_csv('glassdoor.csv',header=0)
df = df.iloc[:,1:]
df['Salary'] = df['Salary'].replace('$','').apply(lambda x: x.split('/')[0])
df['Salary'] = df['Salary'].apply(lambda x: x.replace('$','').replace(',',''))
# Function
def SalaryTrans(x):
    try:
        x = float(x)
        if x >= 1000:
            return x
        else:
            return x * 40 *4 *12
    except:
        return(np.nan)

def TitleTran(x):
    if 'analyst' in x.lower() or 'business' in x.lower() :
        return('Data Analyst')
    elif 'machine' in x.lower():
        return('ML')
    elif 'engineer' in x.lower():
        return('Data Engineer')
    else:
        return('Data Scietist')

def seniority(x):
    if ('sr' in x.lower()) or ('senior' in x.lower()) or ('principal' in x.lower()) or ('lead' in x.lower()) or ('staff' in x.lower()):
        return '1'
    elif ('jr' in x.lower()) or ('junior' in x.lower()):
        return '0'
    else:
        return 'none'
    
def Size(x):
    if x[0] == '1':
        return '10000+'
    elif x == 'NoSize':
        return x
    elif x == 'Unknown':
        return 'NoSize'
    else:
        return str((int(x.split()[0]) + int(x.split()[2]))/2)
    
    
df['Salary'] = df['Salary'].apply(lambda x: SalaryTrans(x) )
df.dropna(subset=['Salary'],inplace=True)
#average working hours a week is 40 hrs, sorucing from google
 
df['Title'] = df['Title'].apply(lambda x: TitleTran(x))   
df['Seniority']= df['Title'].apply(lambda x: seniority(x))
df['Location'] = df['Location'].apply(lambda x: x.split(',')[1] if x != 'Remote' else 'Remote')
df['Size'] = df['Size'].apply(lambda x : Size(x))
df['Revenue'] = df['Revenue'].replace('$','').apply(lambda x: 'NoRevenue' if x[0]=="U" else x)

# Dscrb
df['Python'] = df["Dscrb"].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['R'] = df["Dscrb"].apply(lambda x: 1 if 'r' in x.lower() else 0)
df['SQL'] = df["Dscrb"].apply(lambda x: 1 if 'sql' in x.lower() else 0)
df['Spark'] = df["Dscrb"].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df['Aws'] = df["Dscrb"].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df['Excel'] = df["Dscrb"].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df['PowerBI'] = df["Dscrb"].apply(lambda x: 1 if 'powerbi' in x.lower() else 0)
df['Tableau'] = df["Dscrb"].apply(lambda x: 1 if 'tableau' in x.lower() else 0)

df
