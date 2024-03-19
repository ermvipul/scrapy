import scrapy
import re

class ConstructionSpider(scrapy.Spider):
    name = "construction_new-spider"
    start_urls = ["https://keys.craigslist.org/search/bbb#search=1~thumb~0~0"]

    def parse(self, response):
        # Extracting the contact information from the section with id "postingbody"
        links = response.css('ol').getall()
        # url_regex = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        url_regex = r'https?://[^\s/$.?#].[^\s]*'

        # Function to extract URLs from a string
        def extract_urls(html_string):
            return re.findall(url_regex, html_string)

        # Iterate over each HTML string in the list and extract URLs
        
        for html_string in links:
            urls = extract_urls(html_string)
            for url in urls:
                print(url, "url")

# Run spider: scrapy crawl construction_spider -o output.csv
