import scrapy
import re

class ConstructionSpider(scrapy.Spider):
    name = "construction_spider"
    start_urls = ["https://keys.craigslist.org/aos/d/key-west-free-estimates-mobile-scratch/7727620813.html"]

    def parse(self, response):
        # Extracting the contact information from the section with id "postingbody"
        contact_info = response.css("section#postingbody").xpath(".//text()").getall()
        # Joining all text lines into a single string
        contact_text = " ".join(contact_info)

        # Using regular expressions to extract phone numbers and website URLs
        phone_numbers = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', contact_text)
        website_urls = re.findall(r'www\.[\w\-]+\.com', contact_text)

        # Check if phone_numbers or website_urls is empty, yield None if so
        if not phone_numbers:
            phone_numbers = "None"
        if not website_urls:
            website_urls = "None"

        yield {
            "Phone_Numbers": phone_numbers,
            "Website_URLs": website_urls
        }
        breakpoint()
        # Extract the URL of the next page
        next_page_url = response.css('a.next::attr(href)').get()
        if next_page_url:
            # Create a new request to scrape the next page
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

# Run spider: scrapy crawl construction_spider -o output.csv
