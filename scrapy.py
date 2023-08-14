import scrapy
from selenium import webdriver
import re

class EmailScraper:
    def __init__(self):
        pass

    def extract_emails_from_html(self, html_content):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_regex, html_content)
        return emails

class EmailSpider(scrapy.Spider):
    name = 'email_spider'
    start_urls = ['https://example.com']  # Replace with the starting URL

    def parse(self, response):
        # Initialize the EmailScraper instance
        email_scraper = EmailScraper()

        # Extract emails from the current page's content
        extracted_emails = email_scraper.extract_emails_from_html(response.body.decode('utf-8'))
        for email in extracted_emails:
            yield {'email': email}

        # Follow links to other pages within the same website
        for link in response.css('a::attr(href)').getall():
            if link.startswith('/') or link.startswith('https://example.com'):
                yield scrapy.Request(url=link, callback=self.parse)

# Run the spider using the 'scrapy' command-line tool
