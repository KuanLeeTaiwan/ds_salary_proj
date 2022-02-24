# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 11:40:38 2022

@author: momo8
"""

import pandas as pd
import numpy as np
import glassdoorscraper 
import spacy
from collections import Counter
import matplotlib.pyplot as plt


#keyword = 'Data Scientist'
#path = "C:/Users/momo8/Documents/ds_salary_proj/chromedriver.exe"
#df = glassdoorscraper.glassdoorscraper(path,keyword,10000,30)
#df = pd.DataFrame(df)
#df.to_csv('glassdoor.csv')

df = pd.read_csv('glassdoor.csv',header=0)
df1 = pd.read_csv('glassdoor1.csv',header=0)
df = pd.concat([df,df1],axis=0)
df = df.iloc[:,1:]
#df.to_csv('rawdata.csv')


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
    else:
        return '0'



    
def Size(x):
    if x[0] == '1':
        return '10000+'
    elif x == 'NoSize':
        return x
    elif x == 'Unknown':
        return 'NoSize'
    else:
        return str((int(x.split()[0]) + int(x.split()[2]))/2)

def Location(x):
    if x == 'Remote':
        return x
    elif x == 'NoLocation':
        return x
    elif x == 'Maryland':
        return 'MD'
    elif x == "Nevada":
        return "NV"
    else:
        try:
            return x.split(',')[1]
        except:
            return 'No'

def Revenue(x):
    if x == '$25 to $50 million (USD)':
        return 37.5 #median
    elif x == '$10+ billion (USD)':
        return 10000
    elif x == '$100 to $500 million (USD)':
        return 300
    elif x == '$5 to $10 billion (USD)':
        return 7500
    elif x == '$2 to $5 billion (USD)':
        return 3500
    elif x == '$50 to $100 million (USD)':
        return 75
    elif x == '$10 to $25 million (USD)':
        return 17.5
    elif x == '$5 to $10 million (USD)':
        return 7.5
    elif x == '$500 million to $1 billion (USD)':
        return 5250
    elif x == '$1 to $5 million (USD)':
        return 30000
    else:
        return np.nan

df['Salary'] = df['Salary'].apply(lambda x: SalaryTrans(x) )
df.dropna(subset=['Salary'],inplace=True)
#average working hours a week is 40 hrs, sorucing from google
df['Seniority']= df['Title'].apply(lambda x: seniority(x)) 
df['Seniority2'] = df["Dscrb"].apply(lambda x: '1' if 'years of' in x.lower() else '0')
df['Seniority'] = np.where(((df['Seniority2'] == '1') | (df['Seniority'] == '1')), '1','0')
df['Title'] = df['Title'].apply(lambda x: TitleTran(x))   
df['Location'] = df['Location'].apply(lambda x: Location(x))
df['Size'] = df['Size'].apply(lambda x : Size(x))
df['Revenue'] = df['Revenue'].replace('$','').apply(lambda x: np.nan if x[0]=="U" or x[0]=="N" else x)
df['Revenue'] = df['Revenue'].apply(lambda x: Revenue(x)) 
df['Revenue'].fillna(df['Revenue'].median()) 
# Dscrb
df['Python'] = df["Dscrb"].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['R'] = df["Dscrb"].apply(lambda x: 1 if ',R' in x else 0)
df['SQL'] = df["Dscrb"].apply(lambda x: 1 if 'SQL' in x else 0)
df['Spark'] = df["Dscrb"].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df['Aws'] = df["Dscrb"].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df['Excel'] = df["Dscrb"].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df['PowerBI'] = df["Dscrb"].apply(lambda x: 1 if 'powerbi' in x.lower() else 0)
df['Tableau'] = df["Dscrb"].apply(lambda x: 1 if 'tableau' in x.lower() else 0)

#  impute the row wtih missing value in Industry column based on the freq in Dscrb 
nlp = spacy.load('en_core_web_sm')
dfreq = df.groupby('Industry')['Dscrb'].sum()
dfreq =pd.DataFrame(dfreq)
dfreq = dfreq.drop('NoIndustry')
dfreq = dfreq.reset_index()

dfmissingindustry = df[df['Industry']=='NoIndustry']
ImputeList = []
for i in range(len(dfmissingindustry)):
    search_doc = nlp(dfmissingindustry['Dscrb'].iloc[i])
    A=[]
    for j in range(len(dfreq)):
        main_doc = nlp(dfreq['Dscrb'].iloc[j])      
        A.append((i,dfreq.iloc[j,0],main_doc.similarity(search_doc)))
    ImputeList.append(sorted(A, key=lambda tup: tup[1],reverse=True)[0])
dfmissingindustry.reset_index(inplace=True)
dffilling = pd.DataFrame([x[1] for x in ImputeList])
dffilling= pd.merge(dfmissingindustry,dffilling,left_index=True,right_index=True)
dffilling = dffilling.set_index(keys='index').drop(columns='Industry').rename(columns={0:'Industry'})

dfnew = pd.concat([df[df['Industry']!='NoIndustry'],dffilling],axis=0)
# The industry of missing values in Sector is  Telecommunications
dfnew['Sector'] = dfnew['Sector'].apply(lambda x: 'Telecommunications Services' if x == "NoSector" else x)                 
dfnew.drop(columns=['Seniority2'],inplace=True)
dfnew.to_csv('glassdoorcleaned.csv')                  
                      
                      
# EDA will present on jupyter notebook