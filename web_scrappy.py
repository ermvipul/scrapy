
# web scraping framework
import scrapy
 
# for regular expression
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class MailsSpider(CrawlSpider):
    name = 'mails'
    allowed_domains = ['*']
    start_urls = ['https://www.cqinsulation.com/our-team']

    rules = (
        Rule(LinkExtractor(allow=r''), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', response.text)
        for email in emails:
            if 'bootstrap' not in email:
                yield {
                    'URL':response.url,
                    'Email': email
                    }