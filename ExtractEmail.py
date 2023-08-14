from selenium import webdriver
import re
import dns.resolver

class EmailScraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        options.add_experimental_option('detach', True)
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)  # Replace 'Chrome' with 'Firefox' or other supported browser

    def __del__(self):
        self.driver.quit()

    def extract_emails_from_url(self, url):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.driver.get(url)
        webpage = self.driver.page_source
        emails = re.findall(email_regex, webpage)
        return emails

    def is_valid_email(self, email):
        # Regular expression pattern for basic email validation
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            user, domain = email.split('@')
            # Check if the domain has a valid TLD
            tld_pattern = r'^[a-zA-Z]{2,}$'
            if not re.match(tld_pattern, domain.split('.')[-1]):
                return False
            try:
                dns.resolver.resolve(domain, 'MX')
                return True
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                return False
        else:
            return False

    def extract_valid_emails_from_url(self, url):
        extracted_emails = self.extract_emails_from_url(url)
        valid_emails = [email for email in extracted_emails if self.is_valid_email(email)]
        print("valid_emails", valid_emails)
        return valid_emails


if __name__ == '__main__':
    email_scraper = EmailScraper()
