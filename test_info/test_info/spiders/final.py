import scrapy
import re
import pandas as pd

class ConstructionSpider(scrapy.Spider):
    name = "construction_new-spider_link"
    start_urls = ["https://keys.craigslist.org/search/bbb#search=1~thumb~0~0"]

    def parse(self, response):
        # Extracting the HTML strings containing the links
        links = response.css('ol').getall()
        # Defining the regex pattern to extract URLs
        url_regex = r'https?://[^\s/$.?#].[^\s]*'

        # Function to extract URLs from a string
        def extract_urls(html_string):
            return re.findall(url_regex, html_string)

        # Iterate over each HTML string in the list and extract URLs
        for html_string in links:
            urls = extract_urls(html_string)
            for url in urls:
                # Remove trailing '">'
                url = url.rstrip('">')
                # Make a request to the URL and pass it to the parse_contact function
                yield scrapy.Request(url, callback=self.parse_contact)

    def parse_contact(self, response):
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
            "URL": response.url,  # Include the URL of the page where contact info is found
            "Phone_Numbers": phone_numbers,
            "Website_URLs": website_urls
        }

        # Append data to Excel file
        df = pd.DataFrame({
            "URL": [response.url],
            "Phone_Numbers": [phone_numbers],
            "Website_URLs": [website_urls]
        })

        # Read existing data from Excel file, if it exists
        try:
            existing_df = pd.read_excel("contact_info.xlsx")
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            pass

        # Write the updated DataFrame back to the Excel file
        df.to_excel("contact_info.xlsx", index=False)

        self.log("Data written to contact_info.xlsx")
