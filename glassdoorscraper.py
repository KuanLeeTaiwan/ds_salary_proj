# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 21:59:27 2022

@author: momo8
"""
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd


def glassdoorscraper(path, keyword, num_jobs):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)
    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword 
    driver.get(url)
    jobinfo=[]
    
    while len(jobinfo) < 35:
        time.sleep(5)
        job_buttons = driver.find_elements_by_xpath('//*[@id="MainCol"]/div[1]/ul/li[contains(@class,"react")]')  #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:  
            #time.sleep(2)
            if len(jobinfo) < 35:
                job_button.click()  #You might 
                try:
                    driver.find_element_by_css_selector("[alt='Close']").click()  #clicking to the X.
                except NoSuchElementException:
                    pass
                time.sleep(1)
                try:
                    Name = driver.find_elements_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]')
                    Name = Name[0].text.split('\n')[0]
                except:
                    Name = 'NoName'
                try:
                    Title = driver.find_elements_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[2]')
                    Title = Title[0].text
                except:
                    Title = 'NoTitle'
                try:
                    Location = driver.find_elements_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[3]')
                    Location = Location[0].text
                except:
                    Location = 'NoLocation'
                try:
                    Salary = driver.find_elements_by_xpath('//*[@id="JDCol"]/div/article/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div[1]')
                    Salary = Salary[0].text
                except:
                    Salary = 'NoSalary'
                try:
                    Rating = driver.find_elements_by_xpath('//*[@id="employerStats"]/div[1]/div[1]')
                    Rating = Rating[0].text
                except: 
                    Rating = 'NoRating'  
                Dscrb = driver.find_elements_by_xpath('//*[contains(@id, "JobDesc")]/div/div')
                try:
                    Dscrb = Dscrb[0].text
                except:
                    Dscrb = "NoDscrb"
                    
                #if len(Dscrb) == 0:
                # #   pass
               # else:
                 #   job.append(Dscrb[0].text)
                    #time.sleep(2)
                try:
                    Size = driver.find_elements_by_xpath('//*[@id="EmpBasicInfo"]//span[text()="Size"]/following-sibling::span')
                    Size = Size[0].text
                except:
                    Size='NoSize'
                
                try:
                    Founded = driver.find_elements_by_xpath('//*[@id="EmpBasicInfo"]//span[text()="Founded"]/following-sibling::span')
                    Founded= Founded[0].text
                except:
                    Founded='NoFounded'
                try:
                    Type = driver.find_elements_by_xpath('//*[@id="EmpBasicInfo"]//span[text()="Type"]/following-sibling::span')
                    Type= Type[0].text
                except:
                    Type='NoType'
                try:
                    Industry = driver.find_elements_by_xpath('//*[@id="EmpBasicInfo"]//span[text()="Industry"]/following-sibling::span')
                    Industry = Industry[0].text
                except:
                    Industry = 'NoIndustry'
                try:
                    Sector = driver.find_elements_by_xpath('//*[@id="EmpBasicInfo"]//span[text()="Sector"]/following-sibling::span')
                    Sector = Sector[0].text
                except:
                    Sector = 'NoSector'
                try:
                    Revenue = driver.find_elements_by_xpath('//*[@id="EmpBasicInfo"]//span[text()="Revenue"]/following-sibling::span')
                    Revenue = Revenue[0].text
                except:
                    Revenue = 'NoRevenue'
                
                jobinfo.append({"Name" : Name,
                                "Title": Title,
                                "Location": Location,
                                "Salary": Salary,
                                "Rating": Rating,
                "Size" : Size,
                "Founded" : Founded,
                "Type" : Type,
                "Industry" : Industry,
                "Sector" : Sector,
                "Revenue" : Revenue,
                "Dscrb" : Dscrb})
                
            else:
                break   
        try:
            driver.find_element_by_css_selector("[alt='Close']").click()  #clicking to the X.
        except NoSuchElementException:
            pass
    return jobinfo
    
    
    