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
df['EstimatedSalary'] = df['Salary'].replace('$','').apply(lambda x: x.split('/')[0])
df['EstimatedSalary'] = df['EstimatedSalary'].apply(lambda x: x.replace('$','').replace(',',''))
#Salary
def SalaryTrans(x):
    try:
        x = float(x)
        if x >= 1000:
            return x
        else:
            return x * 40 *4 *12
    except:
        return(np.nan)
    
df['EstimatedSalary'] = df['EstimatedSalary'].apply(lambda x: SalaryTrans(x) )
df.dropna(subset=['EstimatedSalary'],inplace=True)
#average working hours a week is 40 hrs, sorucing from google

#Title
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
        return '1''
    elif ('jr' in x.lower()) or ('junior' in x.lower()):
        return '0'
    else:
        return 'none'
    
df['Title_Trans'] = df['Title'].apply(lambda x: TitleTran(x))   
df['Seniority']= df['Title'].apply(lambda x: seniority(x))




