{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "bf742ad5",
   "metadata": {},
   "outputs": [],
   "source": [
    "from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException\n",
    "from selenium import webdriver\n",
    "import time\n",
    "import pandas as pd\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "88e47e45",
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_jobs(keyword, num_jobs, verbose, path, slp_time):\n",
    "    \n",
    "    '''Gathers jobs as a dataframe, scraped from Glassdoor'''\n",
    "    \n",
    "    #Initializing the webdriver\n",
    "    options = webdriver.ChromeOptions()\n",
    "    \n",
    "    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.\n",
    "    #options.add_argument('headless')\n",
    "    \n",
    "    #Change the path to where chromedriver is in your home folder.\n",
    "    driver = webdriver.Chrome(executable_path=path , options=options)\n",
    "    driver.set_window_size(1120, 1000)\n",
    "\n",
    "    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=\"' + keyword + '\"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'\n",
    "    driver.get(url)\n",
    "    jobs = []\n",
    "\n",
    "    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.\n",
    "\n",
    "        #Let the page load. Change this number based on your internet speed.\n",
    "        #Or, wait until the webpage is loaded, instead of hardcoding it.\n",
    "        time.sleep(slp_time)\n",
    "\n",
    "        #Test for the \"Sign Up\" prompt and get rid of it.\n",
    "        try:\n",
    "            driver.find_element_by_class_name(\"selected\").click()\n",
    "        except ElementClickInterceptedException:\n",
    "            pass\n",
    "\n",
    "        time.sleep(.1)\n",
    "\n",
    "        try:\n",
    "            driver.find_element_by_class_name(\"ModalStyle__xBtn___29PT9\").click()  #clicking to the X.\n",
    "        except NoSuchElementException:\n",
    "            pass\n",
    "\n",
    "        \n",
    "        #Going through each job in this page\n",
    "        job_buttons = driver.find_elements_by_class_name(\"jl\")  #jl for Job Listing. These are the buttons we're going to click.\n",
    "        for job_button in job_buttons:  \n",
    "\n",
    "            print(\"Progress: {}\".format(\"\" + str(len(jobs)) + \"/\" + str(num_jobs)))\n",
    "            if len(jobs) >= num_jobs:\n",
    "                break\n",
    "\n",
    "            job_button.click()  #You might \n",
    "            time.sleep(1)\n",
    "            collected_successfully = False\n",
    "            \n",
    "            while not collected_successfully:\n",
    "                try:\n",
    "                    company_name = driver.find_element_by_xpath('.//div[@class=\"employerName\"]').text\n",
    "                    location = driver.find_element_by_xpath('.//div[@class=\"location\"]').text\n",
    "                    job_title = driver.find_element_by_xpath('.//div[contains(@class, \"title\")]').text\n",
    "                    job_description = driver.find_element_by_xpath('.//div[@class=\"jobDescriptionContent desc\"]').text\n",
    "                    collected_successfully = True\n",
    "                except:\n",
    "                    time.sleep(5)\n",
    "\n",
    "            try:\n",
    "                salary_estimate = driver.find_element_by_xpath('.//span[@class=\"gray small salary\"]').text\n",
    "            except NoSuchElementException:\n",
    "                salary_estimate = -1 #You need to set a \"not found value. It's important.\"\n",
    "            \n",
    "            try:\n",
    "                rating = driver.find_element_by_xpath('.//span[@class=\"rating\"]').text\n",
    "            except NoSuchElementException:\n",
    "                rating = -1 #You need to set a \"not found value. It's important.\"\n",
    "\n",
    "            #Printing for debugging\n",
    "            if verbose:\n",
    "                print(\"Job Title: {}\".format(job_title))\n",
    "                print(\"Salary Estimate: {}\".format(salary_estimate))\n",
    "                print(\"Job Description: {}\".format(job_description[:500]))\n",
    "                print(\"Rating: {}\".format(rating))\n",
    "                print(\"Company Name: {}\".format(company_name))\n",
    "                print(\"Location: {}\".format(location))\n",
    "\n",
    "            #Going to the Company tab...\n",
    "            #clicking on this:\n",
    "            #<div class=\"tab\" data-tab-type=\"overview\"><span>Company</span></div>\n",
    "            try:\n",
    "                driver.find_element_by_xpath('.//div[@class=\"tab\" and @data-tab-type=\"overview\"]').click()\n",
    "\n",
    "                try:\n",
    "                    #<div class=\"infoEntity\">\n",
    "                    #    <label>Headquarters</label>\n",
    "                    #    <span class=\"value\">San Francisco, CA</span>\n",
    "                    #</div>\n",
    "                    headquarters = driver.find_element_by_xpath('.//div[@class=\"infoEntity\"]//label[text()=\"Headquarters\"]//following-sibling::*').text\n",
    "                except NoSuchElementException:\n",
    "                    headquarters = -1\n",
    "\n",
    "                try:\n",
    "                    size = driver.find_element_by_xpath('.//div[@class=\"infoEntity\"]//label[text()=\"Size\"]//following-sibling::*').text\n",
    "                except NoSuchElementException:\n",
    "                    size = -1\n",
    "\n",
    "                try:\n",
    "                    founded = driver.find_element_by_xpath('.//div[@class=\"infoEntity\"]//label[text()=\"Founded\"]//following-sibling::*').text\n",
    "                except NoSuchElementException:\n",
    "                    founded = -1\n",
    "\n",
    "                try:\n",
    "                    type_of_ownership = driver.find_element_by_xpath('.//div[@class=\"infoEntity\"]//label[text()=\"Type\"]//following-sibling::*').text\n",
    "                except NoSuchElementException:\n",
    "                    type_of_ownership = -1\n",
    "\n",
    "                try:\n",
    "                    industry = driver.find_element_by_xpath('.//div[@class=\"infoEntity\"]//label[text()=\"Industry\"]//following-sibling::*').text\n",
    "                except NoSuchElementException:\n",
    "                    industry = -1\n",
    "\n",
    "                try:\n",
    "                    sector = driver.find_element_by_xpath('.//div[@class=\"infoEntity\"]//label[text()=\"Sector\"]//following-sibling::*').text\n",
    "                except NoSuchElementException:\n",
    "                    sector = -1\n",
    "\n",
    "                try:\n",
    "                    revenue = driver.find_element_by_xpath('.//div[@class=\"infoEntity\"]//label[text()=\"Revenue\"]//following-sibling::*').text\n",
    "                except NoSuchElementException:\n",
    "                    revenue = -1\n",
    "\n",
    "                try:\n",
    "                    competitors = driver.find_element_by_xpath('.//div[@class=\"infoEntity\"]//label[text()=\"Competitors\"]//following-sibling::*').text\n",
    "                except NoSuchElementException:\n",
    "                    competitors = -1\n",
    "\n",
    "            except NoSuchElementException:  #Rarely, some job postings do not have the \"Company\" tab.\n",
    "                headquarters = -1\n",
    "                size = -1\n",
    "                founded = -1\n",
    "                type_of_ownership = -1\n",
    "                industry = -1\n",
    "                sector = -1\n",
    "                revenue = -1\n",
    "                competitors = -1\n",
    "\n",
    "                \n",
    "            if verbose:\n",
    "                print(\"Headquarters: {}\".format(headquarters))\n",
    "                print(\"Size: {}\".format(size))\n",
    "                print(\"Founded: {}\".format(founded))\n",
    "                print(\"Type of Ownership: {}\".format(type_of_ownership))\n",
    "                print(\"Industry: {}\".format(industry))\n",
    "                print(\"Sector: {}\".format(sector))\n",
    "                print(\"Revenue: {}\".format(revenue))\n",
    "                print(\"Competitors: {}\".format(competitors))\n",
    "                print(\"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\")\n",
    "\n",
    "            jobs.append({\"Job Title\" : job_title,\n",
    "            \"Salary Estimate\" : salary_estimate,\n",
    "            \"Job Description\" : job_description,\n",
    "            \"Rating\" : rating,\n",
    "            \"Company Name\" : company_name,\n",
    "            \"Location\" : location,\n",
    "            \"Headquarters\" : headquarters,\n",
    "            \"Size\" : size,\n",
    "            \"Founded\" : founded,\n",
    "            \"Type of ownership\" : type_of_ownership,\n",
    "            \"Industry\" : industry,\n",
    "            \"Sector\" : sector,\n",
    "            \"Revenue\" : revenue,\n",
    "            \"Competitors\" : competitors})\n",
    "            #add job to jobs\n",
    "\n",
    "        #Clicking on the \"next page\" button\n",
    "        try:\n",
    "            driver.find_element_by_xpath('.//li[@class=\"next\"]//a').click()\n",
    "        except NoSuchElementException:\n",
    "            print(\"Scraping terminated before reaching target number of jobs. Needed {}, got {}.\".format(num_jobs, len(jobs)))\n",
    "            break\n",
    "\n",
    "    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}