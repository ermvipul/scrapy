import csv
import requests
from bs4 import BeautifulSoup

#url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Product%20Management&location=San%20Francisco%20Bay%20Area&geoId=90000084&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=0'
url = "https://www.linkedin.com/jobs/search/?currentJobId=3826518376&f_I=48&f_JT=C&f_PP=105517665%2C102394087%2C105142029%2C100868799%2C105858804%2C104948205%2C103826715%2C102574077%2C101759449%2C103462227%2C101696514%2C101080674%2C104281466&geoId=101318387&location=Florida%2C%20United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&spellCorrectionEnabled=true"
response = requests.get(url)
print(response, "response")

soup = BeautifulSoup(response.content,'html.parser')
print(soup.text, "soup.text")

job_title = soup.find('h3', class_='base-search-card__title').text
print(job_title, "job_title")