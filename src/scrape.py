import numpy as np
import pandas as pd
from selenium import webdriver
import time

search_term_lst = ['JavaScript', 'Python', 'Accounting', 'Marketing', 'Sales', 'Operations' ]
city_state_dict = {'Boulder': 'CO', 'Denver': 'CO', 'Los Angeles': 'CA', 'New York City': 'NY', 'Seattle': 'WA', 'San Francisco': 'CA', 'Chicago': 'IL', 'Austin': 'TX', 'Houston': 'TX', 'Atlanta': 'GA'}
col_names = ['job_url', 'job_descriptions', 'search_term']
job_desc_df = pd.DataFrame(columns = col_names)

for search_term in search_term_lst:
    for city, state in city_state_dict.items():
        api_url = 'https://www.themuse.com/jobs?keyword=' + search_term + '&job_location=' + city + '%2C%20' + state + '&filter=true'
        print('api_url: ', api_url)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        driver = webdriver.Chrome(executable_path="/Applications/chromedriver", chrome_options=options)
        driver.get(api_url)

        joblinklist = []
        joblinks = driver.find_elements_by_xpath('//*[@href][@role="button"]')
        for job in joblinks:
            joburl = job.get_attribute('href')
            joblinklist.append(joburl)
        print('Finished scraping for URLs for {} in {}, {}: '.format(search_term, city, state))
        print('Found {} URLs for {} in {}, {}'.format(len(joblinklist), search_term, city, state))
        print('URLs for {} in {}, {} (joblinklist): '.format(search_term, city, state), joblinklist)

        for jobpage in joblinklist:
            driver.get(jobpage)
            job_description = driver.find_element_by_class_name('job-post-description').text
            job_desc_df = job_desc_df.append({'job_url': jobpage, 'city': city, 'job_descriptions': job_description, 'search_term': search_term}, ignore_index=True)

        print('Finished scraping for descriptions for {} in {}, {}'.format(search_term, city, state))
    print('{} completed for all locations'.format(search_term))
print('job_desc_df.head(): ', job_desc_df.head())
print('job_desc_df.info(): ', job_desc_df.info())
job_desc_df.to_csv('job_desc_csv_fixed_url.csv', index=False, header=True)
print('All completed!')
time.sleep(4)
driver.close()
