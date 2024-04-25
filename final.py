from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import re
from selenium.common.exceptions import TimeoutException

# Creating a webdriver instance
driver = webdriver.Chrome()
# This instance will be used to log into LinkedIn

# Opening linkedIn's login page
driver.get("https://linkedin.com/uas/login")

# waiting for the page to load
time.sleep(5)

# entering username
username = driver.find_element(By.ID, "username")

# In case of an error, try changing the element
# tag used here.

# Enter Your Email Address
username.send_keys("asnasnasm")

# entering password
pword = driver.find_element(By.ID, "password")
# # In case of an error, try changing the element 
# # tag used here.

# Enter Your Password
pword.send_keys("tyeyehsn")

# Clicking on the log in button
# # Format (syntax) of writing XPath --> 
# # //tagname[@attribute='value']
driver.find_element(By.XPATH, "//button[@type='submit']").click()
headers = ["Profile_url", "Website", "Industry", "Company_size", "Headquarters", "Phone_Number"]

# Write headers to the CSV file
with open('company_info.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(headers)
def scrape_linkedin_company_info(profile_url):
    # In case of an error, try changing the
    # XPath used here
    driver.get(profile_url)
    
    # Scroll the page to load more results
    # start = time.time()
    # while True:
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(3)  # Wait for the page to load
    #     end = time.time()
    #     if round(end - start) > 20:
    #         break
    
    # Extract the page source
    src = driver.page_source
    
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(src, 'html.parser')
    
    # Extract LinkedIn URLs
    linkedin_urls = set()
    li_tags = soup.find('ul', class_='reusable-search__entity-result-list list-style-none')
    if li_tags:
        li_items = li_tags.find_all('li', class_='reusable-search__result-container')
        for li_tag in li_items:
            a_tags = li_tag.find_all('a', class_='app-aware-link')
            if a_tags:
                for a_tag in a_tags:
                    linkedin_url = a_tag.get('href')
                    linkedin_urls.add(linkedin_url)
            span_tag = li_tag.find('span', class_='entity-result__title-text')
            if span_tag:
                a_tag_in_span = span_tag.find('a')
                if a_tag_in_span:
                    linkedin_url_in_span = a_tag_in_span.get('href')
                    linkedin_urls.add(linkedin_url_in_span)
    
    # Function to modify URL
    def modify_url(url):
        if url.endswith('/'):
            return url + 'about'
        else:
            return url + '/about'
    # Initialize an empty list to accumulate data for each page
    page_data = []

    # Scrape data from LinkedIn about pages
    for url in linkedin_urls:
        modified_url = modify_url(url)
        try:
            # Visit the modified URL
            driver.get(modified_url)
            print(f"URL: {modified_url}")
            
            # Extract information from the about page
            about_src = driver.page_source
            about_soup = BeautifulSoup(about_src, 'html.parser')
            about_html = about_soup.find('dl', class_='overflow-hidden')
    
            # Extract company information if available
            if about_html:
                # Extract website
                website_tag = about_html.find('a', href=True)
                website = website_tag.text.strip() if website_tag else 'N/A'
                
                # Extract industry
                industry = about_soup.select_one('dt:-soup-contains("Industry") + dd').get_text(strip=True) if about_soup.select_one('dt:-soup-contains("Industry") + dd') else 'N/A'
                
                # Extract company size
                company_size = about_soup.select_one('dt:-soup-contains("Company size") + dd').get_text(strip=True) if about_soup.select_one('dt:-soup-contains("Company size") + dd') else 'N/A'
                
                # Extract headquarters
                headquarters = about_soup.select_one('dt:-soup-contains("Headquarters") + dd').get_text(strip=True) if about_soup.select_one('dt:-soup-contains("Headquarters") + dd') else 'N/A'
                
                # Extract phone number
                phone_number_tag = about_soup.select_one('dt:-soup-contains("Phone") + dd')
                phone_number_out = phone_number_tag.get_text(strip=True) if phone_number_tag else 'N/A'
                phone_pattern = r"\+?[0-9][- \d()+]+"
                # Find all phone numbers using regular expression
                phone_numbers = re.findall(phone_pattern, phone_number_out)

                # Remove duplicates
                phone_number = list(set(phone_numbers))
    
                print("Data extracted successfully.")
                page_data.append([profile_url,website, industry, company_size, headquarters, phone_number])
            else:
                print("No company information found.")
    
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    with open('company_info.csv', mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(page_data)

    print("Company information for the current page written to CSV successfully.")



for i in range(1, 101):
    # Construct the URL with the current page number
    profile_url = f"<put your url>"

    # Split the URL by the 'page=' parameter
    page_split = profile_url.split('page=')

    # Get the second part after splitting, which contains the page number and other parameters
    page_part = page_split[1]

    # Extract the page number by splitting again using the '&' as separator
    page_number = page_part.split('&')[0]
    scrape_linkedin_company_info(profile_url)
    #breakpoint()
    print(f"Page Number for URL {i}:", page_number)

