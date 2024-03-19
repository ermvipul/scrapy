import scrapy
from scrapy import Selector
import csv

class EmailsSpider(scrapy.Spider):
    name = "emails"
    allowed_domains = ["www.cqinsulation.com"]
    start_urls = ["https://www.cqinsulation.com/our-team"]

    def parse(self, response):
        # Extract CEO name and designation using CSS selectors
        ceo_names = response.css("div.image-caption strong::text").getall()
        designations = response.css("div.image-caption em::text").getall()

        # If CEO names or designations are not found using CSS selector, attempt to extract them from raw HTML
        if not ceo_names or not designations:
            selector = Selector(text=response.text)
            ceo_names = selector.css("p strong::text").getall()
            designations = selector.css("p em::text").getall()

        #breakpoint()
        # Write CEO names and designations to CSV file
        with open('output.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Name', 'Designation'])
            writer.writeheader()
            for ceo_name, designation in zip(ceo_names, designations):
                ceo_name = ceo_name.strip() if ceo_name else None
                print(ceo_name)
                designation = designation.strip() if designation else None
                writer.writerow({'Name': ceo_name, 'Designation': designation})

    def closed(self, reason):
        self.log("Spider closed: %s" % reason)